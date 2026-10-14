"""Behavioral checks for retrieval, exact-source precedence and corpus coverage."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "api_catalog.py"
SPEC = importlib.util.spec_from_file_location("api_catalog", SCRIPT_PATH)
api_catalog = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = api_catalog
SPEC.loader.exec_module(api_catalog)


class LexicalDiscoveryTests(unittest.TestCase):
    def test_comments_strings_and_multiline_signatures(self):
        source = '''// native not_a_native();
/** Preserve the real signature and its Float tag. */
native Float:read_value(const text[] = "{fake, enum}",
    Float:fallback = 0.0);
/* forward not_a_forward(); */
stock bool:try_value(value)
{
    new string[] = "^"native hidden();^"";
    return value != 0;
}
'''
        symbols = api_catalog.parse_include("example.inc", source)
        self.assertEqual([symbol.name for symbol in symbols], ["read_value", "try_value"])
        self.assertIn('Float:fallback = 0.0', symbols[0].signature)
        self.assertEqual(symbols[0].doc_line, 1)
        self.assertGreater(symbols[1].implementation_end_line, symbols[1].end_line)

    def test_enum_arguments_commas_and_documentation(self):
        source = '''enum HookIds
{
    /** Return type: int
     * Params: (const this, Float:damage)
     */
    RG_Example = CALL_REGION(player, 2),
    /** Return type: float */
    m_flExample,
    Value = 1 << 4
};
'''
        symbols = api_catalog.parse_include("example.inc", source)
        entries = {symbol.name: symbol for symbol in symbols}
        self.assertEqual(set(entries), {"HookIds", "RG_Example", "m_flExample", "Value"})
        self.assertEqual(entries["RG_Example"].kind, "hook")
        self.assertEqual(entries["m_flExample"].kind, "member")
        self.assertEqual(entries["RG_Example"].signature, "RG_Example = CALL_REGION(player, 2)")
        self.assertIn("Return type: int", "\n".join(source.splitlines()[entries["RG_Example"].doc_line - 1:entries["RG_Example"].end_line]))

    def test_deprecated_aliases_and_overloads(self):
        source = '''/** Old callback. */
#pragma deprecated Use new_callback instead.
forward old_callback(id);
native Float:operator+(Float:first, Float:second) = floatadd;
stock Float:operator+(Float:first, second) { return first + float(second); }
#define getter getter_safe
#define FLAG(%0) (1 << (%0))
'''
        symbols = api_catalog.parse_include("example.inc", source)
        self.assertTrue(next(symbol for symbol in symbols if symbol.name == "old_callback").deprecated)
        operators = [symbol for symbol in symbols if symbol.name == "operator+"]
        self.assertEqual(len(operators), 2)
        self.assertIn("= floatadd;", operators[0].signature)
        self.assertEqual(next(symbol for symbol in symbols if symbol.name == "FLAG").kind, "macro")

    def test_explicit_project_includes_are_not_merged_with_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "amxmodx.inc"
            path.write_text("native project_only(value);\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                status = api_catalog.run(["find", "project_only", "--include-dir", directory, "--json"])
            result = json.loads(output.getvalue())
            self.assertEqual(status, 0)
            self.assertEqual(result["total"], 1)
            self.assertEqual(Path(result["symbols"][0]["path"]), path)
            output = io.StringIO()
            with redirect_stdout(output):
                status = api_catalog.run(["find", "register_plugin", "--include-dir", directory, "--json"])
            self.assertEqual(status, 1)
            self.assertEqual(json.loads(output.getvalue())["total"], 0)

    def test_raw_search_survives_unsupported_or_broken_declarations(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "custom.inc").write_text("native broken_contract(\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                status = api_catalog.run(["raw", "broken_contract", "--include-dir", directory, "--json"])
            result = json.loads(output.getvalue())
            self.assertEqual(status, 0)
            self.assertEqual(result["total"], 1)
            self.assertEqual(result["matches"][0]["line"], 1)


class BundledCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = api_catalog.load_sources(api_catalog.SNAPSHOT_DIR, [])
        cls.symbols = [symbol for filename, source in cls.sources.items() for symbol in api_catalog.parse_include(filename, source)]
        cls.names = {symbol.name for symbol in cls.symbols}

    def test_known_contracts_across_api_families(self):
        expected = {"RegisterHookChain", "SetHookChainArg", "RG_CBasePlayer_TakeDamage", "m_iTeam", "var_origin", "ATYPE_FLOAT", "RegisterMessage", "MsgArgType", "bind_pcvar_float", "client_disconnected", "SQL_ThreadQuery", "json_parse", "INI_CreateParser", "SMC_CreateParser", "TrieIterCreate", "ArraySortEx", "VTC_OnClientStartSpeak", "RegisterQueryFile", "REU_GetAuthtype", "ns_get_energy", "dod_get_user_class", "tfc_get_user_goalitem", "ts_getuserwpn", "getClientKI", "rg_fire_bullets3", "fmt"}
        self.assertEqual(expected - self.names, set())

    def test_each_supplied_include_has_live_parsed_declarations(self):
        manifest = api_catalog.load_manifest()
        self.assertEqual(set(self.sources), set(api_catalog.ownership(manifest)))
        for filename in self.sources:
            with self.subTest(include=filename):
                self.assertTrue(any(symbol.include == filename for symbol in self.symbols))

    def test_source_ranges_and_documentation_are_within_source(self):
        for symbol in self.symbols:
            with self.subTest(symbol=symbol.name, include=symbol.include):
                self.assertLessEqual(1, symbol.doc_line)
                self.assertLessEqual(symbol.doc_line, symbol.line)
                self.assertLessEqual(symbol.line, symbol.end_line)
                self.assertLessEqual(symbol.end_line, len(self.sources[symbol.include].splitlines()))
                self.assertLessEqual(symbol.end_line, symbol.implementation_end_line)
                self.assertLessEqual(symbol.implementation_end_line, len(self.sources[symbol.include].splitlines()))
                self.assertIn(symbol.name, symbol.signature)

    def test_every_native_forward_and_stock_header_is_discoverable(self):
        for filename, source in self.sources.items():
            masked = api_catalog.mask_source(source)
            header_lines = {api_catalog.line_number(masked, match.start()) for match in re.finditer(r"(?m)^[ \t]*(?:native|forward|stock)[ \t]+", masked)}
            indexed_lines = {symbol.line for symbol in self.symbols if symbol.include == filename and symbol.kind in ("native", "forward", "stock", "stock-variable")}
            with self.subTest(include=filename):
                self.assertEqual(header_lines - indexed_lines, set())

    def test_collection_resources_and_fingerprints(self):
        self.assertEqual(api_catalog.validate_pack(api_catalog.load_manifest()), [])

    def test_relocated_collection_uses_its_own_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "portable-skills"
            shutil.copytree(api_catalog.PACK_DIR, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            script = copied / "cs16-api-reference" / "scripts" / "api_catalog.py"
            validation = subprocess.run([sys.executable, "-B", str(script), "validate", "--json"], capture_output=True, text=True, timeout=20)
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertTrue(json.loads(validation.stdout)["ok"])
            retrieval = subprocess.run([sys.executable, "-B", str(script), "show", "create_cvar", "--json"], capture_output=True, text=True, timeout=20)
            self.assertEqual(retrieval.returncode, 0, retrieval.stdout + retrieval.stderr)
            result = json.loads(retrieval.stdout)
            self.assertEqual(Path(result["source_dir"]), copied / "cs16-api-reference" / "references" / "includes")
            self.assertTrue(Path(result["symbols"][0]["path"]).is_relative_to(copied))


if __name__ == "__main__":
    unittest.main()

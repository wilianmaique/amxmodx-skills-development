#include <amxmodx>

new Float:g_EffectScale;

public plugin_init()
{
    register_plugin("Modern Cvar Example", "1.0.0", "Example");

    new pcvar = create_cvar("example_effect_scale", "1.0", FCVAR_NONE,
        "Scale for the example effect", true, 0.0, true, 5.0);
    bind_pcvar_float(pcvar, g_EffectScale);
    hook_cvar_change(pcvar, "OnEffectScaleChanged");
    AutoExecConfig(true, "example_modern_cvar");
}

public OnConfigsExecuted()
{
    // Derive startup state here after all standard config files have executed.
    server_print("[Example] Configured effect scale: %.2f", g_EffectScale);
}

public OnEffectScaleChanged(pcvar, const old_value[], const new_value[])
{
    // Use new_value directly instead of depending on binding callback order.
    server_print("[Example] Effect scale changed from %s to %s",
        old_value, new_value);
}

#include <amxmodx>
#include <json>

public plugin_init()
{
    register_plugin("JSON Handle Example", "1.0.0", "Example");
}

public OnConfigsExecuted()
{
    new JSON:root = json_parse("{^"effect^":{^"enabled^":true}}");
    if (root == Invalid_JSON)
    {
        log_amx("[Example] Cannot parse configuration.");
        return;
    }

    if (json_get_type(root) != JSONObject
        || !json_object_has_value(root, "effect", JSONObject))
    {
        json_free(root);
        log_amx("[Example] Expected an effect object.");
        return;
    }

    // This getter returns another owned handle, even though it is a child.
    new JSON:effect = json_object_get_value(root, "effect");
    if (effect != Invalid_JSON)
    {
        if (json_object_has_value(effect, "enabled", JSONBoolean))
        {
            server_print("[Example] Effect enabled: %d",
                json_object_get_bool(effect, "enabled"));
        }
        json_free(effect);
    }

    json_free(root);
}

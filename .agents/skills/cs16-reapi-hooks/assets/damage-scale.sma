#include <amxmodx>
#include <reapi>

new Float:g_DamageScale;

public plugin_init()
{
    register_plugin("Damage Scale Example", "1.0.0", "Example");
    if (!is_regamedll())
    {
        set_fail_state("This example requires ReGameDLL_CS.");
        return;
    }

    bind_pcvar_float(create_cvar("example_damage_scale", "1.0", FCVAR_NONE,
        "Multiplier for positive player damage", true, 0.0, true, 10.0),
        g_DamageScale);
    RegisterHookChain(RG_CBasePlayer_TakeDamage, "OnTakeDamagePre", false);
}

public OnTakeDamagePre(const victim, inflictor, attacker,
    Float:damage, bits_damage_type)
{
    if (!is_user_alive(victim) || damage <= 0.0)
    {
        return HC_CONTINUE;
    }

    // Argument 4 is Float damage. Keep the original path and other hooks.
    // Attacker/inflictor may be world or non-player entities; no slot read occurs.
    SetHookChainArg(4, ATYPE_FLOAT, damage * g_DamageScale);
    return HC_CONTINUE;
}

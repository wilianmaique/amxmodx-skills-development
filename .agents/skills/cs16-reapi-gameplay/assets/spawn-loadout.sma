#include <amxmodx>
#include <reapi>

new g_LoadoutEnabled;

public plugin_init()
{
    register_plugin("Spawn Loadout Example", "1.0.0", "Example");
    if (!is_regamedll())
    {
        set_fail_state("This example requires ReGameDLL_CS.");
        return;
    }

    bind_pcvar_num(create_cvar("example_spawn_loadout", "1", FCVAR_NONE,
        "Give a secondary weapon after successful spawn", true, 0.0, true, 1.0),
        g_LoadoutEnabled);
    RegisterHookChain(RG_CBasePlayer_Spawn, "OnPlayerSpawnPost", true);
}

public OnPlayerSpawnPost(const id)
{
    if (!g_LoadoutEnabled || !IsReapiHookOriginalWasCalled(RG_CBasePlayer_Spawn)
        || !is_user_alive(id))
    {
        return HC_CONTINUE;
    }

    new weapon = rg_give_item(id, "weapon_deagle", GT_REPLACE);
    if (weapon > 0)
    {
        rg_set_user_bpammo(id, WEAPON_DEAGLE, 35);
    }

    return HC_CONTINUE;
}

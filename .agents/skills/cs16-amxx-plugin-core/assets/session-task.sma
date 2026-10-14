#include <amxmodx>
#include <amxmisc>

#define TASK_WELCOME 3100

// Example: cancel the task and verify userid before using a reused client slot.
public plugin_init()
{
    register_plugin("Session Task Example", "1.0.0", "Example");
}

public client_putinserver(id)
{
    if (is_user_bot(id) || is_user_hltv(id))
    {
        return;
    }

    new data[2];
    data[0] = id;
    data[1] = get_user_userid(id);
    set_task_ex(5.0, "WelcomeCurrentSession", TASK_WELCOME + id,
        data, sizeof data, SetTask_Once);
}

public client_disconnected(id, bool:drop, message[], maxlen)
{
    remove_task(TASK_WELCOME + id);
}

public WelcomeCurrentSession(const data[], task_id)
{
    new id = data[0];
    if (id < 1 || id > MaxClients || task_id != TASK_WELCOME + id)
    {
        return;
    }

    if (!is_user_connected(id) || get_user_userid(id) != data[1])
    {
        return;
    }

    client_print(id, print_chat, "Welcome to the server.");
}

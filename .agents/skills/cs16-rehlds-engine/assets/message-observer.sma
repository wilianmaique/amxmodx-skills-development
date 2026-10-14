#include <amxmodx>
#include <reapi>

new MessageHook:g_TextMessageHook = INVALID_MESSAGEHOOK;

public plugin_init()
{
    register_plugin("ReHLDS Message Example", "1.0.0", "Example");
    if (!is_rehlds())
    {
        set_fail_state("This example requires the ReHLDS message API.");
        return;
    }

    new message_id = get_user_msgid("TextMsg");
    if (message_id > 0)
    {
        g_TextMessageHook = RegisterMessage(message_id, "OnTextMessagePost", true);
    }
}

public OnTextMessagePost(message_id, destination, recipient)
{
    if (GetMessageArgsNum() < 2 || GetMessageArgType(2) != ArgString)
    {
        return HC_CONTINUE;
    }

    new text[192];
    GetMessageData(MsgArg, 2, text, charsmax(text));
    if (equal(text, "#Game_Commencing"))
    {
        server_print("[Example] Game commencement message %d, dest %d, recipient %d",
            message_id, destination, recipient);
    }

    return HC_CONTINUE;
}

public plugin_end()
{
    if (g_TextMessageHook != INVALID_MESSAGEHOOK)
    {
        UnregisterMessage(g_TextMessageHook);
        g_TextMessageHook = INVALID_MESSAGEHOOK;
    }
}

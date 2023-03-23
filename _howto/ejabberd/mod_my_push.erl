-module(mod_my_push).

-include_lib("xmpp/include/xmpp.hrl").
-include("logger.hrl").
-include("translate.hrl").

%% Every ejabberd module implements the gen_mod behavior
%% The gen_mod behavior requires two functions: start/2 and stop/1
-behaviour(gen_mod).
 
%% API
-export([start/2, stop/1, reload/3, mod_doc/0,
         depends/2, mod_options/1]).

-export([filter_offline_msg/1]).


-spec filter_offline_msg({_, message()}) -> {_, message()}.
filter_offline_msg({_Action, #message{from = From, to = To, id = ID, type = Type} = Msg} = Acc) ->

    %%STo = jid:encode(To),
    STo = To#jid.user,
    ?INFO_MSG("--- ~p", [STo]),
    Acc.

start(_Host, _Opt) -> 
    ?INFO_MSG("mod_my_push loading", []),
    ejabberd_hooks:add(offline_message_hook, _Host, ?MODULE, filter_offline_msg, 150).

stop (_Host) -> 
    ?INFO_MSG("stopping mod_my_push", []),
    ejabberd_hooks:delete(offline_message_hook, _Host, ?MODULE, filter_offline_msg, 150).

reload(_Host, _NewOpts, _OldOpts) ->
    ok.

depends(_Host, _Opts) ->
    [].

mod_options(Host) ->
    [].

mod_doc() ->
    #{desc =>
          ?T("This is an my_push module.")}.

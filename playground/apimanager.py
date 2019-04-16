from threading import Thread, ThreadError, Lock
from traceback import print_exc

from ..LiveCom.SystemComponents.EventBus import EventBus, EventBusError
from time import sleep

# TODO: rewrite this into API standard.

# method: late send signal ( longer latency but reliable. )

sysbus = EventBus()

lock_token_container = dict()
# format: { "lock_token": {"return_context": "val"} }

#example_lock_object = ("return_path_name", Lock())

def request_handler(context: dict):
    try:
        print("ReqCallback: has been called, sleep 4s.")
        sleep(4)
        print("ReqCallback: sleep time out. starting actual processing")
        # unpack request
        # TODO: Maybe this method can be used to construct some API?
        unpacked = context["request"] # can be pack some args and kwargs inside.

        # process result.
        result = unpacked["a"] + unpacked["b"]

        # send back request
        print("ReqCallback: finished processing. Sending result.")
        sysbus.create_event(EventBus.EType.OUTGOING, "test_resp", ["TestResponse"], {
            "returns": result,
            "lock": context["lock"]
        })
        print("ReqCallback: Finished.")

    except:
        print_exc()
        context["lock"][1].release() # force finish task

def response_handler(context):
    print("RespCallback: has been called, store result.")
    return_path = context["lock"][0]
    lock_token_container[return_path] = context["returns"]
    print("RespCallback: stored, releasing lock.")
    context["lock"][1].release()

def test_request_func(a, b):
    lock_token = "test_lock"
    # create request
    req = {
        "a": a,
        "b": b
    }

    # create lock object
    locker = (lock_token, Lock())
    print("Func: Lock setup.")
    locker[1].acquire()
    # pack lock object into request
    print("Func: Send request")
    sysbus.create_event(EventBus.EType.INCOMING, "test_source", ["TestRequest"], {
        "request": req,
        "lock": locker
    })
    print("Func: Wait unlock and responce")
    # wait for response
    locker[1].acquire()
    print("Func: unlocked.")
    locker[1].release()

    # get result from public container, with cleanup.
    ret_val_container = lock_token_container.pop(lock_token)
    return ret_val_container

def Register(sysbus: EventBus):
    sysbus.create_group(EventBus.EType.INCOMING, "TestRequest")
    sysbus.add_listener(EventBus.EType.INCOMING, "TestRequest", "TRequest", request_handler)
    sysbus.create_group(EventBus.EType.OUTGOING, "TestResponse")
    sysbus.add_listener(EventBus.EType.OUTGOING, "TestResponse", "TResponse", response_handler)


# 我在想我这种远程做1+1的做法是不是有点233了...

Register(sysbus)
sysbus.start_loop()
print(test_request_func(1,1))
sysbus.stop_loop()

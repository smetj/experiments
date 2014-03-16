package main

import "wishbone"
import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
// import "wishbone/module/flow/funnel"
import "time"
import "fmt"
import "runtime"

type moduler interface{
    Init()
    GetName() string
    Start()
    Stop()
    Pause()
    GetLogChannel()*chan(actor.Log)
}

func main() {

    runtime.GOMAXPROCS(4)

    router := router.Init()

    input := testevent.Init("input", "one")
    input_instance := moduler(input)
    router.Register(input_instance)

    // input2 := testevent.Init("input2", "two")
    // input3 := testevent.Init("input3", "three")
    // funnel := funnel.Init("funnel")
    output := stdout.Init("output")
    output_instance := moduler(output)
    router.Register(output_instance)

    // input1.Connect("outbox", output.Queuepool["inbox"].Queue)
    // input2.Connect("outbox", funnel.Queuepool["inbox2"].Queue)
    // input3.Connect("outbox", funnel.Queuepool["inbox3"].Queue)
    // funnel.Connect("outbox", output.Queuepool["inbox"].Queue)



    for{
        time.Sleep(time.Second * 1)
    }
    fmt.Println("The end.")
}
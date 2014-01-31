package main

import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
import "wishbone/module/flow/fanout"
import "runtime"

// import "fmt"

func main() {

	runtime.GOMAXPROCS(4)

	router := router.NewRouter()

	input := testevent.NewModule("input", "Hello.")
	fanout := fanout.NewModule("fanout")
	output1 := stdout.NewModule("output1", true)
	output2 := stdout.NewModule("output2", true)
	output3 := stdout.NewModule("output3", true)
	logs := stdout.NewModule("logs", false)

	router.Register(&input)
	router.Register(&fanout)
	router.Register(&output1)
	router.Register(&output2)
	router.Register(&output3)
	router.Register(&logs)

	router.Connect("_internal_logs.outbox", "logs.inbox")

	router.Connect("input.outbox", "fanout.inbox")
	router.Connect("fanout.one", "output1.inbox")
	router.Connect("fanout.two", "output2.inbox")
	router.Connect("fanout.three", "output3.inbox")

	router.Start()
	router.Block()
}

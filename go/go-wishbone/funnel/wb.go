package main

import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
import "wishbone/module/flow/funnel"
import "runtime"

// import "fmt"

func main() {

	runtime.GOMAXPROCS(4)
	router := router.NewRouter()

	input1 := testevent.NewModule("input1", "Hello I am number one.")
	input2 := testevent.NewModule("input2", "Hello I am number two.")
	input3 := testevent.NewModule("input3", "Hello I am number three.")
	funnel := funnel.NewModule("funnel")
	output := stdout.NewModule("output", true)
	logs := stdout.NewModule("logs", false)

	router.Register(&input1)
	router.Register(&input2)
	router.Register(&input3)
	router.Register(&funnel)
	router.Register(&output)
	router.Register(&logs)

	router.Connect("_internal_logs.outbox", "logs.inbox")

	router.Connect("input1.outbox", "funnel.input1")
	router.Connect("input2.outbox", "funnel.input2")
	router.Connect("input3.outbox", "funnel.input3")
	router.Connect("funnel.outbox", "output.inbox")

	router.Start()
	router.Block()
}

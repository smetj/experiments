package main

import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
import "wishbone/module/flow/funnel"
import "wishbone/module/output/tcp"
import "wishbone/module/system/metrics/graphite"
import "runtime"

// import _ "net/http/pprof"
// import "log"
// import "net/http"

// import "fmt"

func main() {

	// go func() {
	// 	log.Println(http.ListenAndServe("localhost:6060", nil))
	// }()

	runtime.GOMAXPROCS(2)
	router := router.NewRouter()

	input1 := testevent.NewModule("input1", "Hello I am number one.")
	input2 := testevent.NewModule("input2", "Hello I am number two.")
	input3 := testevent.NewModule("input3", "Hello I am number three.")
	funnel := funnel.NewModule("funnel")
	output := stdout.NewModule("output", true)

	logs := stdout.NewModule("logs", false)
	graphite := graphite.NewModule("graphite")
	metrics := tcp.NewModule("metrics", "graphite-001:2013", true, true)

	router.Register(&input1)
	router.Register(&input2)
	router.Register(&input3)
	router.Register(&funnel)
	router.Register(&output)
	router.Register(&logs)
	router.Register(&graphite)
	router.Register(&metrics)

	router.Connect("_internal_logs.outbox", "logs.inbox")
	router.Connect("_internal_metrics.outbox", "graphite.inbox")
	router.Connect("graphite.outbox", "metrics.inbox")

	router.Connect("input1.outbox", "funnel.input1")
	router.Connect("input2.outbox", "funnel.input2")
	router.Connect("input3.outbox", "funnel.input3")
	router.Connect("funnel.outbox", "output.inbox")

	router.Start()
	router.Block()
}

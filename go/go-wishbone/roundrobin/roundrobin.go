package main

import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
import "wishbone/module/flow/roundrobin"

func main() {

	router := router.NewRouter()
	input := testevent.NewModule("input", "Hello")
	roundrobin := roundrobin.NewModule("roundrobin")

	output_log := stdout.NewModule("output_log", false)
	output_metric := stdout.NewModule("output_metric", false)

	output1 := stdout.NewModule("output1", true)
	output2 := stdout.NewModule("output2", true)

	router.Register(&input)
	router.Register(&roundrobin)
	router.Register(&output1)
	router.Register(&output2)

	router.Register(&output_log)
	router.Register(&output_metric)

	router.Connect("_internal_logs.outbox", "output_log.inbox")
	router.Connect("_internal_metrics.outbox", "output_metric.inbox")

	router.Connect("input.outbox", "roundrobin.inbox")
	router.Connect("roundrobin.outbox1", "output1.inbox")
	router.Connect("roundrobin.outbox2", "output2.inbox")

	router.Start()
	router.Block()
}

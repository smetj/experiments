package main

import "wishbone/event"



func test(name string, queues ...chan(event.Event) ){
    for{
        output := chan(event.Event)

        for _, c := range queues{
            go func(input chan(event.Event), output chan(event.Event)){
                for{
                    ouput <- input
                }
            }(c, output)
        }
    }
}

func main() {

}
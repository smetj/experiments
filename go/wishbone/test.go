package main
import "fmt"

// type Queue struct{
//     function func(string)
//     queue chan
// }

// type Producer struct{

//     Function func()string
// }

// type Consumer struct{
//     Name string
//     Function func(string)
// }

type Queue struct{
    queue chan(string)
    function interface{}
    total uint64
}

func (q *Queue) Increment(){
    q.total++
}


type Actor struct{
    Queues map[string]*Queue
}

func consume(event string){
    fmt.Println(event)
}

func produce()string{
    return "hello"
}


func main() {
    blurp := new(Actor)
    blurp.Queues = make(map[string]*Queue)
    blurp.Queues["inbox"] = new(Queue)
    blurp.Queues["inbox"].queue = make(chan string)
    blurp.Queues["inbox"].function = produce

    blurp.Queues["inbox"].Increment()
    blurp.Queues["inbox"].function.(func()string)()



    // a := Producer{Name:"test", Function:produce}

    // fmt.Println(a.Name)

    // blurp.queues = make(map[string]interface{})
    // blurp.queues["producer"] = produce
    // blurp.queues["producer"].(func()string)()

    // fmt.Println(blurp.queues["producer"].(Producer).Name)

    // blurp.queues["consumer"] = new(Consumer)
    // blurp.queues["consumer"].Function = consume

    // var blarp interface{} = "hha"


    // switch u := blarp.(type) {
    //     case int:
    //         fmt.Printf("integer", u)
    //     case string:
    //         fmt.Printf("string", u)
    // }
}
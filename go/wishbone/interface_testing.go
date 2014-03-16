package main
import "wishbone/module/input/testevent"
import "fmt"
// import "reflect"

type wrapper interface{
    Init()
    GetName() string
    Start()
}

func blurp(a wrapper){
    fmt.Println(a.GetName())
}

func main() {
    input := testevent.Init("input", "one")
    instance := wrapper(input)
    // fmt.Println(input.Name)
    blurp(instance)
}
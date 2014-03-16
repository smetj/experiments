package main

import "reflect"
import "fmt"

type blah struct{
    a chan int,1
}

func main() {
    kak := blah{}
    kak.a = make(chan int,1)
    fmt.Println(reflect.TypeOf(kak.a).Kind())
}
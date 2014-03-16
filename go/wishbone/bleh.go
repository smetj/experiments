package main

import "fmt"

var m = map[string]struct{x, y int} {
    "foo": {2, 3},
}

func main() {
    m["foo"].x = 4 // cannot assign to m["foo"].x
    fmt.Println(m)
}
package main

import "fmt"

type Actor struct {
	Consumer func()
}

func (a *Actor) Start() {
	fmt.Println("start")
	a.Consumer()
}
func (a *Actor) Stop() {
	fmt.Println("start")
}
func (a *Actor) RegisterConsumer(f func()) {
	a.Consumer = f
}

type Kaka struct {
	Actor
}

func (k *Kaka) Consume() {
	fmt.Println("Consumed")
}

func main() {
	blah := Kaka{}
	blah.RegisterConsumer(blah.Consume)
	blah.Start()
}

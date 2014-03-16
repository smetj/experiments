package main
import "fmt"
import "time"
import "strings"

type Logger interface{
    alert(string)
    critical(string)
    error(string)
    warning(string)
    notice(string)
    info(string)
    debug(string)
}

type QueueLogger struct{
    Name string
    logs chan([4]string)
}

func (l *QueueLogger) alert(message string){
    l.logs <- [4]string{"1", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) critical(message string){
    l.logs <- [4]string{"2", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) error(message string){
    l.logs <- [4]string{"3", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) warning(message string){
    l.logs <- [4]string{"4", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) notice(message string){
    l.logs <- [4]string{"5", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) info(message string){
    l.logs <- [4]string{"6", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}
func (l *QueueLogger) debug(message string){
    l.logs <- [4]string{"7", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}
}

type ScreenLogger struct{
    Name string
}
func (l *ScreenLogger) alert(message string){
    fmt.Println(strings.Join([]string{"1", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) critical(message string){
    fmt.Println(strings.Join([]string{"2", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) error(message string){
    fmt.Println(strings.Join([]string{"3", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) warning(message string){
    fmt.Println(strings.Join([]string{"4", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) notice(message string){
    fmt.Println(strings.Join([]string{"5", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) info(message string){
    fmt.Println(strings.Join([]string{"6", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}
func (l *ScreenLogger) debug(message string){
    fmt.Println(strings.Join([]string{"7", fmt.Sprintf("%d",time.Now().Unix()), l.Name, message}, ", "))
}

type Actor struct{
    Name string
    Logging interface {info(string)}
}

func (a *Actor) init(logs string){
    switch logs {
        case "screen":
            a.Logging = Logger(ScreenLogger{Name: a.Name})
        case "queue":
            a.Logging = Logger(QueueLogger{Name: a.Name, logs: make(chan([4]string))})
        default:
            fmt.Println("shit")
    }
}

func (a *Actor) start(){
    a.Logging.info("ZOMFG")
}


func main() {

    actor := Actor{Name:"hahaha"}
    actor.init("screen")
    actor.start()


}
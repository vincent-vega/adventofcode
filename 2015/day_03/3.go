package main

import (
	"fmt"
	"log"
	"os"
)

type point struct{ x, y int }

func (p point) move(c rune) point {
	switch c {
	case '^':
		p.y--
	case '>':
		p.x++
	case 'v':
		p.y++
	case '<':
		p.x--
	}
	return p
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("usage: go run . <input>")
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	cur := point{0, 0}
	visited := map[point]bool{}
	visited[cur] = true
	for _, c := range string(data) {
		cur = move(c, cur, visited)
	}
	fmt.Println(len(visited)) // 2592

	visited = map[point]bool{}
	curSanta, curRobo := point{0, 0}, point{0, 0}
	visited[curSanta] = true
	for i, c := range string(data) {
		if i%2 == 0 {
			curSanta = move(c, curSanta, visited)
		} else {
			curRobo = move(c, curRobo, visited)
		}
	}
	fmt.Println(len(visited)) // 2360
}

func move(direction rune, cur point, visited map[point]bool) point {
	cur = cur.move(direction)
	visited[cur] = true
	return cur
}

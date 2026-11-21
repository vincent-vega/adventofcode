package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

const size = 1000

type operation int

const (
	on operation = iota + 1
	off
	toggle
)

type instruction struct {
	op             operation
	x1, y1, x2, y2 int
}

func part1(instructions []instruction) int {
	lights := make([]bool, size*size)
	for _, cur := range instructions {
		for y := cur.y1; y <= cur.y2; y++ {
			row := lights[y*size+cur.x1 : y*size+cur.x2+1]
			switch cur.op {
			case on:
				for x := range row {
					row[x] = true
				}
			case off:
				clear(row)
			case toggle:
				for x := range row {
					row[x] = !row[x]
				}
			default:
				panic(fmt.Sprintf("invalid operation %d", cur.op))
			}
		}
	}
	lit := 0
	for _, l := range lights {
		if l {
			lit++
		}
	}
	return lit
}

func part2(instructions []instruction) int {
	lights := make([]int, size*size)
	for _, cur := range instructions {
		for y := cur.y1; y <= cur.y2; y++ {
			row := lights[y*size+cur.x1 : y*size+cur.x2+1]
			switch cur.op {
			case on:
				for x := range row {
					row[x]++
				}
			case off:
				for x := range row {
					row[x] = max(0, row[x]-1)
				}
			case toggle:
				for x := range row {
					row[x] += 2
				}
			default:
				panic(fmt.Sprintf("invalid operation %d", cur.op))
			}
		}
	}
	brightness := 0
	for _, b := range lights {
		brightness += b
	}
	return brightness
}

func parse(line string) (instruction, error) {
	var opName string
	var current instruction
	_, err := fmt.Sscanf(strings.TrimPrefix(line, "turn "), "%s %d,%d through %d,%d", &opName, &current.x1, &current.y1, &current.x2, &current.y2)
	if err != nil {
		return current, fmt.Errorf("parse %q: %w", line, err)
	}
	switch opName {
	case "on":
		current.op = on
	case "off":
		current.op = off
	case "toggle":
		current.op = toggle
	default:
		return current, fmt.Errorf("parse %q: unknown operation %q", line, opName)
	}
	return current, nil
}

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("usage: %s <input>", os.Args[0])
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	var instructions []instruction
	for sc.Scan() {
		cur, err := parse(sc.Text())
		if err != nil {
			log.Fatal(err)
		}
		instructions = append(instructions, cur)
	}
	if err := sc.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println(part1(instructions))
	fmt.Println(part2(instructions))
}

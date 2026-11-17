package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func paper(l, w, h int) int {
	a, b, c := l*w, l*h, w*h
	return min(a, b, c) + 2*(a+b+c)
}

func ribbon(l, w, h int) int {
	return l*w*h + 2*min(l+w, l+h, w+h)
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
	var part1, part2 int
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		var l, w, h int
		if _, err := fmt.Sscanf(sc.Text(), "%dx%dx%d", &l, &w, &h); err != nil {
			log.Fatal(err)
		}
		part1 += paper(l, w, h)
		part2 += ribbon(l, w, h)
	}
	if err := sc.Err(); err != nil {
		panic(err)
	}
	fmt.Println(part1) // 1598415
	fmt.Println(part2) // 3812909
}

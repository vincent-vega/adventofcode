package main

import (
	"bytes"
	"crypto/md5"
	"fmt"
	"log"
	"os"
	"strconv"
)

func mine(key []byte, zeros, start int) int {
	buf := append([]byte(nil), key...)
	for n := start; ; n++ {
		sum := md5.Sum(strconv.AppendInt(buf[:len(key)], int64(n), 10))
		if hasZeroPrefix(sum, zeros) {
			return n
		}
	}
}

func hasZeroPrefix(sum [md5.Size]byte, n int) bool {
	for i := 0; i < n/2; i++ {
		if sum[i] != 0 {
			return false
		}
	}
	return n%2 == 0 || sum[n/2]>>4 == 0
}

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("usage: %s <input>", os.Args[0])
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	key := bytes.TrimSpace(data)

	part1 := mine(key, 5, 1)
	part2 := mine(key, 6, part1)
	fmt.Println(part1) // 117946
	fmt.Println(part2) // 3938038
}

package main

import (
	"fmt"
	"os"
)

func main() {
	categoricalMode := true
	commands := os.Args[1:]

	if len(commands) > 1 {
		help("Only one argument!")
		os.Exit(125)
	}

	for _, command := range commands {
		if command == "--rec" || command == "--rig" || command == "-r" {
			categoricalMode = false
		} else if command == "--cat" || command == "-c" {
			categoricalMode = true
		} else if command == "--range" || command == "--ran" || command == "-R" {
			fmt.Println("The only range is ALL THE RANGE")
		}
	}

	if !categoricalMode {
		fmt.Println("Starting in recursive mode.")

	} else {
		fmt.Println("Starting in categorical mode.")
		categoricalTest()
	}

	fmt.Println("I workd?")
}

func help(message string) {
	fmt.Println(message)
	fmt.Println("minepkgStressTest [ARGS]")
	fmt.Println("Rigorous: --rig, --rec, -r -- Test literally every version of minecraft available.")
	fmt.Println("Categorically [default]: --cat, -c -- Test the latest patch version of every minor version of minecraft, if that patch fails repeat with the next latest patch.")
}

func categoricalTest() {
	rdList := []string{"rd-161348", "rd-20090515", "rd-132211"}
	cList := []string{"c0.0.11a", "c0.30_01a"}
	infList := []string{"inf-20100618"}
	aList := []string{"a1.2.6", "a1.2.2a", "a1.1.0", "a1.0.15", "a1.0.4"}

	bList := [9]string{"b1.8.1", "b1.7.3", "b1.6.6", "b1.5_01", "b1.4_01", "b1.3_01", "b1.2_02", "b1.1_02", "b1.0"}
	// TODO: alphaList := rdList + cList + infList + aList

	alphaList := append(aList, infList...)
	alphaList = append(alphaList, cList...)
	alphaList = append(alphaList, rdList...)

	fmt.Println(alphaList)
	fmt.Println(bList)
}

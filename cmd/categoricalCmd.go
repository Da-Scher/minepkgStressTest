package cmd

import (
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"
	"syscall"
	"time"

	"github.com/spf13/cobra"
)

var (
	versionRange []string

	categoricalCmd = &cobra.Command{
		Use:   "categorical",
		Short: "Test versions smarter",
		Long:  "Test versions from latest patch of minor, down.",
		Run: func(cmd *cobra.Command, args []string) {
			processVersions()
		},
	}
)

func init() {
	rootCmd.AddCommand(categoricalCmd)

}

/*
	startCategoryTest(version string) -- loop through all the

*
*/
func startCategoryTest(version string) {
	fmt.Println("Categorical test starts here.")
	waitChan := make(chan error)

	testCommand := exec.Command("minepkg", "launch", "vanilla", "--minecraft", version)
	detector := NewLogDetector()
	mw := io.MultiWriter(os.Stdout, detector)
	testCommand.Stdout = mw
	testCommand.Stderr = mw

	if err := testCommand.Start(); err != nil {
		panic(err)
	}

	defer testCommand.Process.Signal(syscall.SIGTERM)
	go func() {
		waitChan <- testCommand.Wait()
	}()
	//fmt.Print("\n\nHELLO\n\n")
	select {
	case <-detector.found:
		fmt.Println("The Duck Digs Dirt")
		time.Sleep(time.Second)
		// Stop the process
	case <-waitChan:
		break
	case <-time.After(15 * time.Second):
		log.Printf("%s :: Minecraft did not exit, stopping '''peacefully'''\n", version)
	}

	fmt.Println("> minepkgStressTest")

}

type prog struct {
}

func processVersions() {
	url := "https://launchermeta.mojang.com/mc/game/version_manifest.json"

}

type logDetector struct {
	found chan bool
}

func (l *logDetector) Write(p []byte) (n int, err error) {
	if strings.Contains(string(p), "[Render thread/INFO]: Created: 128x128x0 minecraft:textures/atlas/bom_effects.png-atlas") {
		log.Println("[StressTest]: Important string found!")
		l.found <- true
	}
	return len(p), nil
}

func NewLogDetector() *logDetector {
	return &logDetector{
		found: make(chan bool),
	}
}

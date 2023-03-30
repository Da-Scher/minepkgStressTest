package cmd

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"

	"github.com/spf13/cobra"
)

var (
	versionRange []string

	categoricalCmd = &cobra.Command{
		Use:   "categorical",
		Short: "Test versions smarter",
		Long:  "Test versions from latest patch of minor, down.",
		Run: func(cmd *cobra.Command, args []string) {
			startCategoryTest()
		},
	}
)

func init() {
	rootCmd.AddCommand(categoricalCmd)

}

func startCategoryTest() {
	fmt.Println("Categorical test starts here.")
	testCommand := exec.Command("minepkg", "launch", "vanilla")
	var stdBuffer bytes.Buffer
	mw := io.MultiWriter(os.Stdout, &stdBuffer)
	testCommand.Stdout = mw
	testCommand.Stderr = mw
	if err := testCommand.Run(); err != nil {
		panic(err)
	}

	fmt.Println("> minepkgStressTest")

	log.Println(stdBuffer.String())
}

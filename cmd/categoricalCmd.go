package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var categoricalCmd = &cobra.Command{
	Use:   "categorical",
	Short: "Test versions smarter",
	Long:  "Test versions from latest patch of minor, down.",
	Run: func(cmd *cobra.Command, args []string) {
		startCategoryTest()
	},
}

func init() {
	rootCmd.AddCommand(categoricalCmd)
}

func startCategoryTest() {
	fmt.Println("Categorical test starts here.")
}

package cmd

import (
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	// Used for flags
	userLicense string

	rootCmd = &cobra.Command{
		Use:   "minepkgStressTest",
		Short: "Test a bunch of minecraft versions locally via minepkg.",
		Long: `minepkgStressTest is a program that runs a bunch of minecraft 
versions to demonstrate if they work or not.`,
	}
)

func Execute() error {
	return rootCmd.Execute()
}

func init() {
	cobra.OnInitialize()

	rootCmd.PersistentFlags().BoolP("license", "l", false, "Display build license")

	viper.BindPFlag("viperLicense", rootCmd.PersistentFlags().Lookup("license"))
}

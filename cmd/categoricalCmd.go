package cmd

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strconv"
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
			versionsList := listVersions()
			//var versionsTest []bool
			for i := 0; i <= 5; i++ {
				switch versionsList[i].Type {
				case "release":
					releaseParser(versionsList[i])
					//versionsTest = append(versionsTest, startCategoryTest(versionsList[i]))
					break
				default:
					break
				}
			}
		},
	}
)

func init() {
	rootCmd.AddCommand(categoricalCmd)

}

func releaseParser(version jsonVersions) {
	state := 0
	minor := ""
	patch := ""
	// seperate by "."'s
	for i := 0; i < len(version.Id); i++ {
		// if a dot is detected, change state and skip.
		if string(version.Id[i]) == "." {
			state += 1
			continue
		}
		// probably unnecessary to check major versions.
		if state == 1 {
			minor += string(version.Id[i])
			continue
		} else if state == 2 {
			patch += string(version.Id[i])
			continue
		}
	}
	fmt.Printf("major: 1\nminor: %s\npatch: %s\n", minor, patch)
	if startCategoryTest("1." + minor + "." + patch) {
		algoMinor, err := strconv.Atoi(minor)
		if err != nil {
			panic(err)
		}

		algoMinor -= 1

		minor = string(algoMinor)

	}
}

/*
	startCategoryTest(version string) -- loop through all the

*
*/
func startCategoryTest(version string) bool {
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
	select {
	case <-detector.found:
		fmt.Println("The Duck Digs Dirt")
		time.Sleep(time.Second)
		return true
		// Stop the process
	case <-waitChan:
		break
	case <-time.After(15 * time.Second):
		log.Printf("%s :: Minecraft did not exit, stopping '''peacefully'''\n", version)
		return true
	}

	fmt.Println("> minepkgStressTest")
	return false

}

type jsonVersions struct {
	Id          string
	Type        string
	Url         string
	Time        string
	ReleaseTime string
}

func listVersions() []jsonVersions {
	// get data from https://launchermeta.mojang.com/mc/game/version_manifest.json
	url := "https://launchermeta.mojang.com/mc/game/version_manifest.json"
	res, err := http.Get(url)
	if err != nil {
		panic(err)
	}

	//error handling
	defer res.Body.Close()

	// read json response
	// TODO: do something with error
	byt, err := ioutil.ReadAll(res.Body)
	//error handling
	if err != nil {
		panic(err)
	}
	var data map[string]interface{}
	if err := json.Unmarshal([]byte(byt), &data); err != nil {
		panic(err)
	}

	//fmt.Println(data)
	versionsData, err := json.Marshal(data["versions"])
	if err != nil {
		panic(err)
	}
	//fmt.Println(versionsData)
	var versionsList []jsonVersions
	if err := json.Unmarshal([]byte(versionsData), &versionsList); err != nil {
		panic(err)
	}
	//fmt.Println(versionsMap[0].Id)
	return versionsList
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

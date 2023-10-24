// Package config provides utilities to retrieve information
// about the current environment configuration.
package config

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

// OllamaHome returns the value of the OLLAMA_HOME environment variable or the user's home directory if OLLAMA_HOME is not set.
func OllamaHome() (string, error) {
	if home, exists := os.LookupEnv("OLLAMA_HOME"); exists {
		dir, err := os.Stat(home)
		if err != nil {
			if errors.Is(err, os.ErrNotExist) {
				return "", fmt.Errorf("OLLAMA_HOME is set to %q but that directory does not exist", home)
			}
			return "", fmt.Errorf("failed to validate OLLAMA_HOME directory %q: %w", home, err)
		}
		if !dir.IsDir() {
			return "", fmt.Errorf("OLLAMA_HOME is set to %q but that is not a directory", home)
		}
		return home, nil
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(home, ".ollama"), nil
}

// IsPruneDisabled returns true if the OLLAMA_NOPRUNE environment variable is set.
func IsPruneDisabled() bool {
	return os.Getenv("OLLAMA_NOPRUNE") != ""
}

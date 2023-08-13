package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/joho/godotenv"
)

var (
	TOKEN         string
	GPT_SECRET_KEY string
	SK_TOKEN      string
	CATALOG_ID    string
	ALLOWED_USERS []int64
	TEXT_VOICE    string
	MAN_VOICE     string
)

func init() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	TOKEN = os.Getenv("TOKEN")
	GPT_SECRET_KEY = os.Getenv("GPT_SECRET_KEY")
	SK_TOKEN = os.Getenv("SK_TOKEN")
	CATALOG_ID = os.Getenv("CATALOG_ID")

	users := strings.Split(os.Getenv("ADMINS"), ",")
	for _, user := range users {
		var userID int64
		_, err := fmt.Sscan(user, &userID)
		if err != nil {
			log.Fatalf("Error parsing user id: %v", err)
		}
		ALLOWED_USERS = append(ALLOWED_USERS, userID)
	}

	// Initialize other variables ...
}

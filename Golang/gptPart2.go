func handleUpdates(bot *tgbotapi.BotAPI) {
	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates, err := bot.GetUpdatesChan(u)
	if err != nil {
		log.Fatal(err)
	}

	for update := range updates {
		if update.Message == nil {
			continue
		}

		// Check if user is allowed
		isAllowed := false
		for _, userID := range ALLOWED_USERS {
			if update.Message.From.ID == int(userID) {
				isAllowed = true
				break
			}
		}

		if !isAllowed {
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Вы не допущены к использованию тестового бота...")
			bot.Send(msg)
			continue
		}

		// Handle commands
		if update.Message.IsCommand() {
			handleCommand(update.Message, bot)
		} else {
			// Handle normal messages...
		}
	}
}

func handleCommand(message *tgbotapi.Message, bot *tgbotapi.BotAPI) {
	switch message.Command() {
	case "start":
		// handle start...
	case "help":
		// handle help...
	}
}

from controller import GamePlay
import pyinputplus as pyip





if __name__ == "__main__":
    game = GamePlay()
    option = pyip.inputMenu(["sign in", "sign up"],
                            prompt="enter an option(1-2):\n",
                            numbered=True)
    game.define_user(option)
    recommend = pyip.inputYesNo("do you want to be recommended a question type")
    if recommend == "no":
        type = pyip.inputMenu(list(game.types.keys()),
                              prompt="enter question type (1-6):\n",
                              numbered=True)
    else:
        type = None
    game.get_question_type(recommend, type)
    while True:
        game.gen_question()
        user_answer = "!"
        while user_answer not in game.question.plausible_answers:
            if game.question.allowed_types[game.type_acr] == "int":  # question parent class has no attribute allowed
                # types but its subclasses do. here the question type is already estblished in gen question.
                user_answer = int(input(f'{game.question.question_phrase} {game.question.plausible_answers}'))
            else:
                user_answer = input(f'{game.question.question_phrase} {game.question.plausible_answers}')
        game.set_answer(user_answer)
        game.update_scores()
        go = input("continue?")
        if go == "no":
            break
        same_type = input("same type?")
        if same_type == "no":
            game.update_recorded_scores()
            game.correct = 0
            game.incorrect = 0
            recommend = pyip.inputYesNo("do you want to be recommended a question type")
            if recommend == "no":
                type = pyip.inputMenu(list(game.types.keys()),
                                      prompt="enter question type (1-6):\n",
                                      numbered=True)
            else:
                type = None
            game.get_question_type(recommend, type)

    print(f"GAME OVER")
    print(f"correct: {game.correct}")
    print('incorrect: {game.incorrect}')
    game.update_recorded_scores()
    game.user.save_details_dict_to_json()
    game.user.sign_out()


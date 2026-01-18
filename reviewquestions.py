#key : (list_of_options, id, name)
survey_data = {
        "PRODUCTIVITY": {
            "Is there Wi-Fi": ([("No", "low"), ("Yes, but can be unstable or limited", "medium"), ("Definitely, it's very reliable!", "high")], "wifi"),
            "Is it easy to find power sockets": ([("No (< 10% of seats have power sockets)", "low"), ("So-so (10-50% of seats have power sockets)", "medium"), ("Definitely (> 50% of seats have power sockets)", "high")], "sockets"),
            "How long can you comfortably stay and work?": ([("While eating or drinking only", "low"), ("Depends on how busy it gets", "medium"), ("I can stay as long as i want!", "high")], "duration"),
            "Are tables and chairs comfortable for work ?": ([("No (or very small amount)", "low"), ("somewhat / it,s", "medium"), ("All tables and chairs are work friendly!", "high")], "tables"),
            "Is it quiet?": ([("No", "low"), ("So-so / Depends", "medium"), ("Definitely!", "high")], "quiet"),
            "Can you comfortably make audio/video calls?": ([("No", "low"), ("Maybe / Depends", "medium"), ("Definitely", "high")], "audio")
        },
        "COMMUNITY": {
            "Is it common to see other people working?": ([("No, nobody is working", "low"), ("Yes, some people are working", "medium"), ("Definitely, almost everyone is working!", "high")], "people-working"),
            "Are there group tables (for 6+ people)": ([("No", "low"), ("Yes", "medium"), ("Definitely! There's also a big community table", "high")], "group-tables")
        },
        "SERVICE": {
            "Is coffee available": ([("No", "low"), ("Yes, but average quality", "medium"), ("Yes, and its of high quality!", "high")], "coffee-available"),
            "Is food offered": ([("No", "low"), ("Only snacks, pastries, or salads", "medium"), ("Definitely, proper meals!", "high")], "food-offered"),
            "Are there veggie options": ([("No", "low"), ("Yes, but limited", "medium"), ("Definitely, with great veggie meals!", "high")], "veggie-options"),
            "Is alcohol offered": ([("No", "low"), ("Only a small selection (Beers, wines, ciders)", "medium"), ("Definitely, a wide selection (Liquors, cocktails, etc.)", "high")], "alcohol-offered"),
            "Are credit cards accepted?": ([("No", "low"), ("Only some cards or amounts", "medium"), ("Definitely!", "high")], "credit-cards")
        },
        "SPACE": {
            "Is the space full of natural light": ([("No", "low"), ("So-so / Only some areas", "medium"), ("Definitely!", "high")], "natural-light"),
            "Is there an outdoor area? (Assuming nice weather)": ([("No", "low"), ("Yes, but without power sockets", "medium"), ("Yes, with outdoor power sockets available too!", "high")], "outdoor-area"),
            "How large is the place ?": ([("it's small (less than 10 tables)", "low"), ("it's medium (between 10 and 30 tables)", "medium"), ("it's large (more than 30 tables)", "high")], "large-space"),
            "Is there a restroom": ([("No", "low"), ("Yes, but far away, dirty, or inconvenient", "medium"), ("Definitely, it's clean and easily accessible!", "high")], "restroom"),
            "Is it easily accessible with a wheelchair": ([("No", "low"), ("So-So", "medium"), ("Definitely", "high")], "wheelchair-access"),
            "Is the place air conditioned?": ([("No", "low"), ("Only a small area (less than half of the tables)", "medium"), ("Definitely, most or all areas are air conditioned!", "high")], "air-conditioned"),
            "Is the space smoke free": ([("No", "low"), ("There is a non-smoking area", "medium"), ("Definitely!", "high")], "smoke-free"),
            "Is it pet friendly": ([("No", "low"), ("Only some areas (e.g outdoors)", "medium"), ("Definitely", "high")], "pet-friendly"),
            "Is there a parking space": ([("No", "low"), ("There's street parking nearby", "medium"), ("There is dedicated parking!", "high")], "parking-space")
        },
        "SUMMARY": {
            "In general, do you like working from here?": ([("No it's uncomfortable for work", "0"), ("Yes, I got some work done", "50"), ("Definitely, I feel very productive here!", "100")], "summary")
        }
    }

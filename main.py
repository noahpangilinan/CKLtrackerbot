import discord
import os # default module

from discord.enums import try_enum
from dotenv import load_dotenv
from utils import load_data, add_ckl_race, format_user_race_data, get_avg_placement, get_avg_points, log
from discord.ext import commands
from discord.ui import Button, View

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

def races():
    return {
        "MKS":"Mario Kart Stadium",
        "WP":"Water Park",
        "SSC":"Sweet Sweet Canyon",
        "TR":"Thwomp Ruins",
        "MC":"Mario Circuit",
        "TH":"Toad Harbor",
        "TM":"Twisted Mansion",
        "SGF":"Shy Guy Falls",
        "SA":"Sunshine Airport",
        "DS":"Dolphin Shoals",
        "ED":"Electrodome",
        "MW":"Mount Wario",
        "CC":"Cloudtop Cruise",
        "BDD":"Bone-Dry Dunes",
        "BC":"Bowser's Castle",
        "RR":"Rainbow Road",
        "rMMM":"Moo Moo Meadows",
        "rMC":"Mario Circuit",
        "rCCB":"Cheep Cheep Beach",
        "rTT":"Toad's Turnpike",
        "rDDD":"Dry Dry Desert",
        "rDP3":"Donut Plains 3",
        "rRRY":"Royal Raceway",
        "rDKJ":"DK Jungle",
        "rWS":"Wario Stadium",
        "rSL":"Sherbert Land",
        "rMP":"Music Park",
        "rYV":"Yoshi Valley",
        "rTTC":"Tick-Tock Clock",
        "rPPS":"Piranha Plant Slide",
        "rGV":"Grumble Volcano",
        "rRRD":"Rainbow Road",
        "dYC":"Yoshi Circuit",
        "dEA":"Excitebike Arena",
        "dDD":"Dragon Driftway",
        "dMC":"Mute City",
        "dWGM":"Wario's Gold Mine",
        "dRR":"SNES Rainbow Road",
        "dIIO":"Ice Ice Outpost",
        "dHC":"Hyrule Circuit",
        "dBP":"Baby Park",
        "dCL":"Cheese Land",
        "dWW":"Wild Woods",
        "dAC":"Animal Crossing",
        "dNBC":"Neo Bowser City",
        "dRIR":"Ribbon Road",
        "dSBS":"Super Bell Subway",
        "dBB":"Big Blue",
        "bPP":"Paris Promenade",
        "bTC":"Toad Circuit",
        "bCMo":"Choco Mountain",
        "bCMa":"Coconut Mall",
        "bTB":"Tokyo Blur",
        "bSR":"Shroom Ridge",
        "bSG":"Sky Garden",
        "bNH":"Ninja Hideaway",
        "bNYM":"New York Minute",
        "bMC3":"Mario Circuit 3",
        "bKD":"Kalimari Desert",
        "bWP":"Waluigi Pinball",
        "bSS":"Sydney Sprint",
        "bSL":"Snow Land",
        "bMG":"Mushroom Gorge",
        "bSHS":"Sky-High Sundae",
        "bLL":"London Loop",
        "bBL":"Boo Lake",
        "bRRM":"Rock Rock Mountain",
        "bMT":"Maple Treeway",
        "bBB":"Berlin Byways",
        "bPG":"Peach Gardens",
        "bMM":"Merry Mountains",
        "bRR7":"3DS Rainbow Road",
        "bAD":"Amsterdam Drift",
        "bRP":"Riverside Park",
        "bDKS":"DK Summit",
        "bYI":"Yoshi's Island",
        "bBR":"Bangkok Rush",
        "bMC":"DS Mario Circuit",
        "bWS":"Waluigi Stadium",
        "bSSy":"Singapore Speedway",
        "bAtD":"Athens Dash",
        "bDC":"Daisy Cruiser",
        "bMH":"Moonview Highway",
        "bSCS":"Squeaky Clean Sprint",
        "bLAL":"Los Angeles Laps",
        "bSW":"Sunset Wilds",
        "bKC":"Koopa Cape",
        "bVV":"Vancouver Velocity",
        "bRA":"Rome Avanti",
        "bDKM":"DK Mountain",
        "bDCt":"Daisy Circuit",
        "bPPC":"Piranha Plant Cove",
        "bMD":"Madrid Drive",
        "bRIW":"Rosalina's Ice World",
        "bBC3":"Bowser Castle 3",
        "bRRW":"Wii Rainbow Road",
    }


# Autocomplete function for the `user` parameter
async def race_autocomplete(ctx: discord.AutocompleteContext):
    return [race for race in races().keys() if ctx.value.lower() in race.lower()][:25]






@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="help", description="Get information on available commands")
async def help(ctx: discord.ApplicationContext):
    help_message = (
        "**CKL Bot Commands Help**\n\n"
        "Here’s a list of available commands and how to use them:\n\n"

        "🏁 **/add_ckl_race**\n"
        "Add a list of placements for a specific race.\n"
        "Usage: `/add_ckl_race race:<race_name> placements:<Name1, Place1; Name2, Place2>`\n"
        "_Example: `/add_ckl_race race:Mario Kart placements:Noah, 1; Gabe, 2`_\n\n"

        "📊 **/show_raw_race_data**\n"
        "Display detailed race data for a specific user and race.\n"
        "Usage: `/show_raw_race_data user:<username> race:<race_name>`\n"
        "_Example: `/show_raw_race_data user:Noah race:Mario Kart`_\n\n"

        "📈 **/ckl_stats**\n"
        "Show overall CKL stats for a specific user, including average placement, best and worst tracks.\n"
        "Usage: `/ckl_stats user:<username>`\n"
        "_Example: `/ckl_stats user:Noah`_\n\n"
        
        "🏆 **/find_best_team_races**\n"
        "Identify the top-performing tracks as a team based on average points.\n"
        "Usage: `/find_best_team_races count:<number>`\n"
        "_Example: `/find_best_team_races count:3`_\n"
        "Displays the best tracks for the team by averaging points across users and scaling to a 6-person team.\n\n")
    await ctx.respond(help_message)

    help_message = (

        "🏆 **/best**\n"
        "Show the best races for a specific user, based on either placements or points.\n"
        "Usage: `/best user:<username> by:<Placements|Points> count:<number>`\n"
        "_Example: `/best user:Noah by:Points count:5`_\n\n"
    
        "🚫 **/worst**\n"
        "Display the worst races for a specific user, based on either placements or points.\n"
        "Usage: `/worst user:<username> by:<Placements|Points> count:<number>`\n"
        "_Example: `/worst user:Noah by:Placements count:3`_\n\n"
    
        "🔍 **/compare**\n"
        "Compare the performance of two users in a specific race.\n"
        "Usage: `/compare user1:<username1> user2:<username2> race:<race_name>`\n"
        "_Example: `/compare user1:Noah user2:Gabe race:Mario Kart`_\n\n"
    
        "📊 **/compare_all**\n"
        "Compare the performance of all users in a specific race.\n"
        "Usage: `/compare_all race:<race_name>`\n"
        "_Example: `/compare_all race:Mario Kart`_\n\n"
    
        "✨ **/rarest**\n"
        "Show the races that a specific user has played the least.\n"
        "Usage: `/rarest user:<username> count:<number>`\n"
        "_Example: `/rarest user:Noah count:3`_\n\n"
    
        "🌟 **/most_frequent**\n"
        "Show the races that a specific user has played the most.\n"
        "Usage: `/most_frequent user:<username> count:<number>`\n"
        "_Example: `/most_frequent user:Noah count:5`_\n\n"
    )

    await ctx.send( help_message)
    log(f"{ctx.author} - help(): 200 OK")


class ConfirmButtonView(View):
    def __init__(self, confirm_placements, confirm_race):
        super().__init__()
        self.confirm_placements = confirm_placements
        self.confirm_race = confirm_race

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button, interaction):
        add_ckl_race(placements=self.confirm_placements, race=self.confirm_race)
        await interaction.message.edit(content="Race logged successfully!", view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_callback(self, button, interaction):
        # Edit the message to remove the view, making buttons disappear
        await interaction.message.edit(content="Action canceled.", view=None)
        self.stop()





@bot.slash_command(name="add_ckl_race", description="Add a list of placements for a user")
async def add_placements(
        ctx: discord.ApplicationContext,
        race: discord.Option(str, "Select a race", autocomplete=race_autocomplete),
        placements: str):
    """
    Parameters:
        race (str): The race identifier (e.g., race name or ID)
        placements (str): A semicolon-separated list of name, place entries (e.g., "Name1, Place1; Name2, Place2")
    """
    try:
        # Parse the placements string into a list of tuples
        placements_list = []
        for entry in placements.split(";"):
            name, place = entry.split(",")
            placements_list.append((name.strip(), place.strip()))

        # Load current data and check for new users
        data = load_data()
        new_users = []

        for user, _ in placements_list:
            if user not in data:
                new_users.append(user)  # Track new users        print(new_users)
        # If there are new users, prompt for confirmation
        warning_message = ""

        if new_users:
            # Show confirmation message with buttons
            warning_message += f"**__Warning__**: The following new user(s) will be added:\n\n{'\n'.join(new_users)}\n\n"
            # Construct the warning message to confirm the race and placements for each user



        # Construct the warning message to confirm the race and placements for each user
        warning_message += (
                f"Is the following data correct for the race '{race}'?\n\n"
                "Placements:\n" + "\n".join(
            [f"{name}: {place}" for name, place in placements_list])
        )
        view = ConfirmButtonView(placements_list, race)
        await ctx.respond(warning_message, view=view)
        log(f"{ctx.author} - add_ckl_race({race}, {placements}): 200 OK")

    except ValueError:
        await ctx.respond("Error: Please format placements as 'Name, Place; Name2, Place2'")
        log(f"{ctx.author} - show_race_data({race}, {placements}): 404 User Not Found")

    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - show_race_data({race}, {placements}): 500 Internal Error")


# Autocomplete function for the `user` parameter
async def user_autocomplete(ctx: discord.AutocompleteContext):
    data = load_data()
    users = data.keys()
    # Filter usernames based on the partial input
    return [user for user in users if ctx.value.lower() in user.lower()][:25]  # Limit to 25 results

@bot.slash_command(name="show_raw_race_data", description="Show race data for a specific user")
async def show_race_data(ctx: discord.ApplicationContext,
                         user: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
                         race: discord.Option(str, "Select a race", autocomplete=race_autocomplete)):
    try:
        # Convert the formatted string into a list of tuples
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)

        def ordinal(n):
            """Convert an integer to an ordinal string."""
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return str(n) + suffix

        pretty_dict_str = f"**Race Results for:** {user}\n\n"  # Bold heading for user
        user_str = ""

        # Convert placements to ordinal strings
        placements_str = ', '.join(
            ordinal(place) for place in data[user][race])  # Create a readable string for placements
        race_name = races()[race]
        user_str += f"**Race:** {race_name} ({race})  \n"  # Bold race name with line break
        user_str += f"**Placements:** {placements_str}  \n\n"  # Bold placements with line break

        user_str += f"**Average Placement:** {get_avg_placement(user = user, track = race)}\n"  # Bold placements with line break
        user_str += f"**Average Points:** {get_avg_points(user = user, track = race)}"  # Bold placements with line break


        pretty_dict_str += user_str
        await ctx.respond(pretty_dict_str)
        log(f"{ctx.author} - show_race_data({user}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - show_race_data({user}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - show_race_data({user}): 500 Internal Error")



@bot.slash_command(name="ckl_stats", description="Show race data for a specific user")
async def ckl_stats(ctx: discord.ApplicationContext, user: discord.Option(str, "Select a user", autocomplete=user_autocomplete)):
    try:
        # Convert the formatted string into a list of tuples
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)
        race_avgs = []
        race_points_avgs = []

        total_races = 0
        for race in data[user].keys():
            total_races += len(data[user][race])

        for race in data[user].keys():
            race_avgs.append((race, get_avg_placement(user=user,track=race)))
            race_points_avgs.append((race, get_avg_points(user=user,track=race)))
        race_avgs = sorted(race_avgs, key=lambda tup: tup[1])
        race_points_avgs = sorted(race_points_avgs, key=lambda tup: tup[1])

        mean_points = round( sum(elt[1] for elt in race_points_avgs) / len(race_points_avgs), 2)

        mean = round( sum(elt[1] for elt in race_avgs) / len(race_avgs), 2)

        stats_message = (
            f"**🏁 CKL Stats for {user} 🏁**\n\n"
            
            f"**Total CKL Races Played:** {total_races}\n"
            f"**Average Placement Across All Races:** {mean}\n"
            f"**Average Points Across All Races:** {mean_points}\n\n"

            "- **Best Track by Placement:**\n"
            f"  - 🥇 **{race_avgs[0][0]} ({races()[race_avgs[0][0]]})** — Average Placement: {race_avgs[0][1]}\n"
            "- **Worst Track by Placement:**\n"
            f"  - 🥉 **{race_avgs[-1][0]} ({races()[race_avgs[-1][0]]})** — Average Placement: {race_avgs[-1][1]}\n\n"

            "- **Best Track by Points:**\n"
            f"  - 🥇 **{race_points_avgs[-1][0]} ({races()[race_points_avgs[-1][0]]})** — Average Points: {race_points_avgs[-1][1]}\n"
            "- **Worst Track by Points:**\n"
            f"  - 🥉 **{race_points_avgs[0][0]} ({races()[race_points_avgs[0][0]]})** — Average Points: {race_points_avgs[0][1]}"
        )

        await ctx.respond(stats_message)
        log(f"{ctx.author} - ckl_stats({user}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - ckl_stats({user}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - ckl_stats({user}): 500 Internal Error")




@bot.slash_command(name="compare", description="Show race data for specific users and race")
async def compare(ctx: discord.ApplicationContext,
                user1: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
                user2: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
                race: discord.Option(str, "Select a race", autocomplete=race_autocomplete)):
    try:
        # Convert the formatted string into a list of tuples
        data = load_data()

        if user1 not in data.keys():
            raise ValueError(user1)
        if user2 not in data.keys():
            raise ValueError(user2)


        # Initialize string with track information
        user_str = f"**🏎️ Track:** {races()[race]} ({race})\n\n"

        # Get average points and placements for each user
        user1_avg_points = get_avg_points(user=user1, track=race)
        user2_avg_points = get_avg_points(user=user2, track=race)
        user1_avg_place = get_avg_placement(user=user1, track=race)
        user2_avg_place = get_avg_placement(user=user2, track=race)
        user1_play_count = len(data[user1][race])
        user2_play_count = len(data[user2][race])

        # Determine which user has the higher average points and order results
        if user1_avg_points > user2_avg_points:
            # User1 is the winner
            winner_str = (
                f"**🏆 {user1}**\n"
                f"-------------------------\n"
                f"- **Average Placement:** {user1_avg_place}\n"
                f"- **Average Points:** {user1_avg_points}\n"
                f"- *Played {user1_play_count} times*\n\n"
            )
            runner_up_str = (
                f"**{user2}**\n"
                f"-------------------------\n"
                f"- **Average Placement:** {user2_avg_place}\n"
                f"- **Average Points:** {user2_avg_points}\n"
                f"- *Played {user2_play_count} times*\n"
            )
        else:
            # User2 is the winner
            winner_str = (
                f"**🏆 {user2}**\n"
                f"-------------------------\n"
                f"- **Average Placement:** {user2_avg_place}\n"
                f"- **Average Points:** {user2_avg_points}\n"
                f"- *Played {user2_play_count} times*\n\n"
            )
            runner_up_str = (
                f"**{user1}**\n"
                f"-------------------------\n"
                f"- **Average Placement:** {user1_avg_place}\n"
                f"- **Average Points:** {user1_avg_points}\n"
                f"- *Played {user1_play_count} times*\n"
            )

        # Combine winner and runner-up strings into the final user_str
        user_str += winner_str + runner_up_str

        # Respond with the formatted message
        await ctx.respond(user_str)
        log(f"{ctx.author} - compare({user1}, {user2}, {race}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - compare({user1}, {user2}, {race}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - compare({user1}, {user2}, {race}): 500 Internal Error")



@bot.slash_command(name="compare_all", description="Show race data for all users for a race")
async def compare_all(ctx: discord.ApplicationContext,
                race: discord.Option(str, "Select a race", autocomplete=race_autocomplete)):
    await ctx.defer()
    try:
        # Convert the formatted string into a list of tuples
        data = load_data()

        def ordinal(n):
            """Convert an integer to an ordinal string."""
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return str(n) + suffix

        total_race_avgs = ("N/A", "N/A", "N/A",)
        total = 0
        times_played = 0
        player_count = 0
        for user in data.keys():
            if race in data[user].keys():
                total += get_avg_points(user, race)
                player_count += 1
                if len(data[user][race]) > times_played:
                    times_played = len(data[user][race])
                # Calculate average team points for a 6-player team
        if player_count != 0:
            team_points = round(total / (player_count / 6), 2)
            total_race_avgs = (race, team_points, times_played)
        user_str = f"**🏁 Race Results for '{races()[race]}' 🏁**\n\n"
        user_str += f"**Average Team Points:** {total_race_avgs[1]}\n"
        user_str += f"*Times Played: {total_race_avgs[2]}*\n"
        sorted_users = sorted(
            data.keys(),
            key=lambda u: get_avg_placement(user=u, track=race) if race in data[u] else float('inf')
        )
        for idx, user in enumerate(sorted_users):
            if race in data[user]:
                placements_str = ', '.join(ordinal(place) for place in data[user][race])  # Format placements
                avg_placement = get_avg_placement(user=user, track=race)
                avg_points = get_avg_points(user=user, track=race)
                times_played = len(data[user][race])

                # Assign medal emoji based on position
                medal = ""
                if idx == 0:
                    medal = " 🥇"  # First place
                elif idx == 1:
                    medal = " 🥈"  # Second place
                elif idx == 2:
                    medal = " 🥉"  # Third place

                user_str += f"{medal}**{user}**\n"
                user_str += f"   **Average Placement:** {avg_placement}\n"
                user_str += f"   **Average Points:** {avg_points}\n"
                user_str += f"   **Placements:** {placements_str}\n"
                user_str += f"   *Played {times_played} times*\n"
                user_str += f"{'-' * 30}\n\n"  # Separator for clarity

        await ctx.respond(user_str)
        log(f"{ctx.author} - compare_all({race}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - compare_all({race}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - compare_all({race}): 500 Internal Error")

async def by_autocomplete(ctx: discord.AutocompleteContext):
    by =  ["Placements", "Points"]
    return [by for by in by if ctx.value.lower() in by.lower()][:25]  # Limit to 25 results


@bot.slash_command(name="best", description="Show best races")
async def best(ctx: discord.ApplicationContext,
               user: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
               by: discord.Option(str, "Choose 'Placements' or 'Points'", autocomplete=by_autocomplete),
               count: int):
    try:
        # Load data and validate the user
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)

        # Prepare race data lists
        race_avgs = []
        race_points_avgs = []

        # Populate average placements and points for each race
        for race in data[user].keys():
            times_played = len(data[user][race])
            race_avgs.append((race, get_avg_placement(user=user, track=race), times_played))
            race_points_avgs.append((race, get_avg_points(user=user, track=race), times_played))

        # Sort lists based on user's choice
        race_avgs = sorted(race_avgs, key=lambda tup: tup[1])[:count]
        race_points_avgs = sorted(race_points_avgs, key=lambda tup: tup[1], reverse=True)[:count]

        # Helper function to create ordinal (1st, 2nd, etc.)
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return str(n) + suffix

        # Formatting the response
        user_str = f"**🏆 Best Races by {by} for {user} 🏆**\n\n"
        if by == "Points":
            for i, (race, avg_points, times_played) in enumerate(race_points_avgs, start=1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
                race_name = races().get(race, race)  # Get race name or default to the race ID
                user_str += (f"{medal} **{ordinal(i)} {race_name}**\n"
                             f"   - **Average Points:** {avg_points}\n"
                             f"   - *Played {times_played} times*\n"
                             f"{'-' * 30}\n\n")

        elif by == "Placements":
            for i, (race, avg_place, times_played) in enumerate(race_avgs, start=1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
                race_name = races().get(race, race)
                user_str += (f"{medal} **{ordinal(i)} {race_name}**\n"
                             f"   - **Average Placement:** {avg_place}\n"
                             f"   - *Played {times_played} times*\n"
                             f"{'-' * 30}\n\n")

        await ctx.respond(user_str)
        log(f"{ctx.author} - best({user},{by},{count}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - best({user},{by},{count}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - best({user},{by},{count}): 500 Internal Error")



@bot.slash_command(name="worst", description="Show worst races")
async def worst(ctx: discord.ApplicationContext,
               user: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
               by: discord.Option(str, "Choose 'Placements' or 'Points'", autocomplete=by_autocomplete),
               count: int):
    try:
        # Load data and validate the user
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)
        if count > len(data[user].keys()):
            count = len(data[user].keys())

        # Prepare race data lists
        race_avgs = []
        race_points_avgs = []

        # Populate average placements and points for each race
        for race in data[user].keys():
            times_played = len(data[user][race])
            race_avgs.append((race, get_avg_placement(user=user, track=race), times_played))
            race_points_avgs.append((race, get_avg_points(user=user, track=race), times_played))

        # Sort lists based on user's choice
        race_avgs = sorted(race_avgs, key=lambda tup: tup[1], reverse=True)[:count]
        race_points_avgs = sorted(race_points_avgs, key=lambda tup: tup[1])[:count]

        # Helper function to create ordinal (1st, 2nd, etc.)
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return str(n) + suffix

        # Formatting the response
        user_str = f"**🤮 Worst Races by {by} for {user} 🤮**\n\n"
        if by == "Points":
            for i, (race, avg_points, times_played) in enumerate(race_points_avgs, start=1):
                medal = "🛑" if i == 1 else "⚠️" if i == 2 else "💔" if i == 3 else ""
                race_name = races().get(race, race)  # Get race name or default to the race ID
                user_str += (f"{medal} **{ordinal(i)} {race_name}**\n"
                             f"   - **Average Points:** {avg_points}\n"
                             f"   - *Played {times_played} times*\n"
                             f"{'-' * 30}\n\n")

        elif by == "Placements":
            for i, (race, avg_place, times_played) in enumerate(race_avgs, start=1):
                medal = "🛑" if i == 1 else "⚠️" if i == 2 else "💔" if i == 3 else ""
                race_name = races().get(race, race)
                user_str += (f"{medal} **{ordinal(i)} {race_name}**\n"
                             f"   - **Played {times_played} times**\n"
                             f"   - *Average Placement: {avg_place}*\n"
                             f"{'-' * 30}\n\n")

        await ctx.respond(user_str)
        log(f"{ctx.author} - worst({user},{by},{count}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - worst({user},{by},{count}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - worst({user},{by},{count}): 500 Internal Error")


def split_message(message, max_length=2000):
    # Split the message into chunks of specified max_length
    return [message[i:i + max_length] for i in range(0, len(message), max_length)]

@bot.slash_command(name="rarest", description="Show rarest races")
async def rarest(ctx: discord.ApplicationContext,
               user: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
               count: int):
    try:
        # Load data and validate the user
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)
        if count > len(data[user].keys()):
            count = len(data[user].keys())
        # Prepare race data lists
        race_avgs = []

        # Populate average placements and points for each race
        for race in data[user].keys():
            times_played = len(data[user][race])
            race_avgs.append((race, get_avg_placement(user=user, track=race), times_played))

        # Sort lists based on user's choice
        race_avgs = sorted(race_avgs, key=lambda tup: tup[2])[:count]

        user_str = f"Tracks with the fewest plays for {user}\n\n"

        # Formatting the response

        for i, (race, avg_place, times_played) in enumerate(race_avgs, start=1):
            race_name = races().get(race, race)
            line = (f"**{i}. {race_name}**\n"
                    f"**Played {times_played} times**\n"
                    f"*Average Placement: {avg_place}*\n"
                    f"{'-' * 30}\n")

            # Check if adding this line exceeds the length limit
            if len(user_str) + len(line) > 2000:
                # Split and send the current user_str before adding the new line
                messages = split_message(user_str)
                for msg in messages:
                    await ctx.respond(msg)
                user_str = line  # Start a new string with the current line
            else:
                user_str += line  # Add the line to the user_str

        # Send any remaining message
        if user_str:
            messages = split_message(user_str)
            for msg in messages:
                await ctx.respond(msg)

        log(f"{ctx.author} - rarest({user},{count}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - rarest({user},{count}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - rarest({user},{count}): 500 Internal Error")




@bot.slash_command(name="most_frequent", description="Show most frequent races")
async def most_frequent(ctx: discord.ApplicationContext,
               user: discord.Option(str, "Select a user", autocomplete=user_autocomplete),
               count: int):
    try:
        # Load data and validate the user
        data = load_data()
        if user not in data.keys():
            raise ValueError(user)

        # Prepare race data lists
        race_avgs = []

        # Populate average placements and points for each race
        for race in data[user].keys():
            times_played = len(data[user][race])
            race_avgs.append((race, get_avg_placement(user=user, track=race), times_played))

        # Sort lists based on user's choice
        race_avgs = sorted(race_avgs, key=lambda tup: tup[2], reverse=True)[:count]

        user_str = f"Tracks with the most plays for {user}\n\n"

        # Formatting the response

        for i, (race, avg_place, times_played) in enumerate(race_avgs, start=1):
            race_name = races().get(race, race)
            line = (f"**{i}. {race_name}**\n"
                    f"**Played {times_played} times**\n"
                    f"*Average Placement: {avg_place}*\n"
                    f"{'-' * 30}\n")

            # Check if adding this line exceeds the length limit
            if len(user_str) + len(line) > 2000:
                # Split and send the current user_str before adding the new line
                messages = split_message(user_str)
                for msg in messages:
                    await ctx.respond(msg)
                user_str = line  # Start a new string with the current line
            else:
                user_str += line  # Add the line to the user_str

        # Send any remaining message
        if user_str:
            messages = split_message(user_str)
            for msg in messages:
                await ctx.respond(msg)

        log(f"{ctx.author} - most_frequent({user},{count}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - most_frequent({user},{count}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - most_frequent({user},{count}): 500 Internal Error")


@bot.slash_command(name="find_best_team_races", description="Show best team races")
async def find_best_team_races(ctx: discord.ApplicationContext,
               count: int):
    await ctx.defer()
    try:
        # Load data
        data = load_data()

        # Prepare race data
        total_race_avgs = []
        for race in races().keys():
            total = 0
            times_played = 0
            player_count = 0
            for user in data.keys():
                if race in data[user].keys():
                    total += get_avg_points(user, race)
                    player_count += 1
                    if len(data[user][race]) > times_played:
                        times_played = len(data[user][race])


            # Calculate average team points for a 6-player team
            if player_count != 0:
                team_points = round(total / (player_count / 6), 2)
                total_race_avgs.append((race, team_points, times_played))

        # Sort races by team points in descending order
        race_avgs = sorted(total_race_avgs, key=lambda tup: tup[1], reverse=True)

        # Build the response string
        user_str = "**🏆 Best RIT Track(s):**\n\n"
        for i in range(min(count, len(race_avgs))):
            track_id, avg_points = race_avgs[i][0], race_avgs[i][1]
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else str(i+1)

            # Add formatted track data
            line = (
                f"**{medal}. {races()[track_id]} ({track_id})**\n"
                f"**Average Team Points:** {avg_points}\n"
                f"*Times Played: {race_avgs[i][2]}*\n"
                f"{'-' * 30}\n\n"
            )

            if len(user_str) + len(line) > 2000:
                # Split and send the current user_str before adding the new line
                messages = split_message(user_str)
                for msg in messages:
                    await ctx.respond(msg)
                user_str = line  # Start a new string with the current line
            else:
                user_str += line  # Add the line to the user_str

        # Send any remaining message
        if user_str:
            messages = split_message(user_str)
            for msg in messages:
                await ctx.respond(msg)

        log(f"{ctx.author} - find_best_team_races({count}): 200 OK")  # Successful response
    except ValueError as ve:
        await ctx.respond(f"Error: User not found: {str(ve)}")
        log(f"{ctx.author} - find_best_team_races({count}): 404 User Not Found")  # Specific user not found
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
        log(f"{ctx.author} - find_best_team_races({count}): 500 Internal Error")



bot.run(os.getenv('TOKEN')) # run the bot with the token


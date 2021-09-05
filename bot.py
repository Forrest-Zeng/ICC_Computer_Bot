from discord import Client, Intents, Embed, File, Colour, ChannelType, AuditLogAction, Status, ActivityType, Activity
from discord.utils import escape_markdown as escape
from discord_slash import SlashCommand, SlashContext, ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle, SlashCommandPermissionType
from random import choice
from urllib.parse import quote_plus
import requests, schedule, asyncio, datetime, ship_parser, io, re #, shutil, cv2, pytesseract


bot = Client(Intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)
guilds = [800120401107746846]
test_guilds = [842931029701427251]

@bot.event
async def on_ready():
  print("Bot Ready!")
  # setting a custom status (https://github.com/discord/discord-api-docs/issues/1160)
  # asset = (await bot.fetch_guild(800120401107746846)).icon_url
  # activity = Activity(details="Watching over the ICC!", state="Watching over the ICC!", name="Watching over the ICC!", assets={"large_image": asset, "small_image": asset, "large_text": "Watching over the ICC in all it's glory.", "small_text": "Watching over the Irvine Coding Club (as a moderation bot, fun bot, and all around great bot."}, large_image_url="https://irvinecoding.club/assets/images/favicon.png", small_image_url="https://irvinecoding.club/assets/images/favicon.png", large_image_text="Watching over the ICC in all it's glory.", small_image_text="Watching over the Irvine Coding Club (as a moderation bot, fun bot, and all around great bot.", start=datetime.datetime(2021, 1, 16, hour=21, minute=52, second=49, microsecond=142), emoji=str(bot.get_emoji(847338149238800394)))

  await bot.change_presence(status=Status.online, activity=Activity(type=ActivityType.watching, name="over the ICC!"))

#   channel = await bot.fetch_channel(867982690031394827)
#   message = await channel.fetch_message(881900546590662696)
#   embed = message.embeds[0].to_dict()
#   index = list(map(lambda field: field["name"] == "Attendees", embed["fields"])).index(True)
#   embed["fields"][index]["value"] = '''- <@!521575534011088916>
# - <@!769007255700897822>
# - <@!745408105503785010>
# - <@!738900809810575390>
# - <@!451588543618220042>'''
#   await message.edit(embed=Embed.from_dict(embed))


@bot.event
async def on_member_join(member):
  pass  # maybe send to verify or something


@slash.slash(
    name="verify",
    description="Verify your account.",
    guild_ids=guilds,
    options=[
        create_option(
            name="firstname",
            description="Your first name.",
            option_type=3,
            required=True,
        ),
        create_option(name="lastname",
                      description="Your last name.",
                      option_type=3,
                      required=True),
        create_option(
            name="grade",
            description="What grade you're in.",
            option_type=4,
            required=True,
        ),
        create_option(
            name="school",
            description="What school you go to.",
            option_type=3,
            required=True,
        ),
        create_option(
            name="email",
            description="What your email is (personal). (optional)",
            option_type=3,
            required=False,
        ),
        create_option(
            name="referral",
            description="How did you find out about us? (optional)",
            option_type=3,
            required=False,
        ),
    ],
)
async def verify(ctx: SlashContext,
                 firstname,
                 lastname,
                 grade,
                 school,
                 referral="None",
                 email="Not Provided"):
  if (ctx.channel.name != "verify" or any(
      list(map(lambda e: e.id == 839941660942270464, ctx.author.roles)))) and not ctx.author.id == 738900809810575390: # Tim
    await ctx.send("You've already been verified!", hidden=True)
    return
  logs = None
  for _channel in ctx.guild.channels:
    if _channel.name == "icc-logs":
      logs = _channel
      break
  if logs == None:
    await ctx.send(
        "Command must be done inside the ICC server! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  try:
    e = Embed(title="Application", colour=15062910)
    e.add_field(name="First Name", value=firstname)
    e.add_field(name="Last Name", value=lastname)
    e.add_field(name="Grade", value=grade)
    e.add_field(name="School", value=school)
    e.add_field(name="Email", value=email)
    e.add_field(name="Member", value=ctx.author.mention)
    e.add_field(name="Referral", value=referral)
    e.add_field(name="Verified", value="No")
    await logs.send(
      embed=e,
      components=[
          create_actionrow(
              create_button(style=ButtonStyle(3),
                            label="Accept Application",
                            custom_id="accept_application")),
          create_actionrow(
              create_button(style=ButtonStyle(4),
                            label="Deny Application",
                            custom_id="deny_application"))
      ]
    )
  except:
    await logs.send([firstname, lastname, grade, school, referral])
  await ctx.send("You're application is awaiting approval! Please wait at most a few hours to have it approved.", hidden=True)


# permissions for verified
""",
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }"""


# permissions for admin
""",
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }"""

@slash.slash(
    name="prelude",
    description="Get a picture of the cutest doggo ever.",
    guild_ids=guilds,
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def prelude(ctx: SlashContext):
  preludes = [
      "https://cdn.discordapp.com/attachments/838805399162716190/848327737599852554/QFYOqx8AnHKJIHZliGeIBPeRaoO3i-YVUa_rF20bFPRkL3K1LxIwMSUYzb1KTcFNskppYuo8jyjOWmF9v8etKvIECuxSmOPzkj0r.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327840432521246/t7i6HA57SxRGezGs4oMEmcdmgW3zWfnSEHUPx7yPoQu-4Iq42NgPcr9I1Wv-fh-943ndC95pTbCF9EAViaUw_90mzP6pyFi7u3je.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327844081565727/akwkdGoC9KBq72dHxuq00wP4uL2ekOG-nQk9ssrXccP9MdkU6xoXsqBx6p0oxAxdWmDfWSHf8I5pY5GMKsudkl-b4GmVdkCucchm.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327845143248926/2G_ji_-QpvNSZnOWt1KS1kkX4AWmpxvVCEiJjIcy6GhyOLz9Sf9IO27_4ZBn4AmfzT9eLB7ckTYuP9KBzAHFjbNyRB6hUegFKrm9.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327891448365086/yr6Je-omEMbo_kVtwVRVrvEpwZBvYuezDfJnn2ji1Mh46lCP0Nu_pbYF4Q8ZvFzjeo6O7Jb999-7bcWIaW3lEHTzLMJZUciL5ID2.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327891448365086/yr6Je-omEMbo_kVtwVRVrvEpwZBvYuezDfJnn2ji1Mh46lCP0Nu_pbYF4Q8ZvFzjeo6O7Jb999-7bcWIaW3lEHTzLMJZUciL5ID2.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328328699314186/r59rXgxtSVyelztQErzHInOCxIDwYcZrsTbUrmdVX6EpVAbXwErXui8L0EGNlGzhZgLxla9wsoBl7mqujfFIK_keVOUb_PQzzMbz.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328371489472562/fWOKrMMrJXPvQXSYr1UVmhCSuA3o5DlAP_ieZCRnOtUknizK411sWbCDLCF_RS8pwZZrJDr5zLTcTQ0G5YbtC0duvra7CGn7T0_a.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328415467929640/Eakx4kTtZZy32DHes7UzyTJEznVhgkDTDDXClsE4IVF6T7FyzBivmoh_Muoi9UsifvUwd4X_52vhz2SIFxS5fBLVmH3mqv5gLVxD.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328456122925086/mUA5X20Qo6omnrYSzTMRniZukZnMtltqoqp8mqKzqstwXG_VOE0iIPYCx2JT7ee_UDv3BxEsj3R-pvT4TRJbAdMajU8Wgg5YPu9z.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328557264764978/o8sa9VEaK1EJyVhcItTojizrw8OYglw05PDqCB84uj6uF2Ll9jlxEOie-AOpIoq9p9SR0WyixjWsOPKHTgV4xR4VHiHrmtxk0Um5.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328589777961021/-OEoGmagOx9osKooCw0udJyiqHmvwJxcQO-RVuhqViBxOI_orIDHMjubmlQDaxc68eL39Zt81iG_vu9BXkFKrVww6R9U58kVy-tc.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328665137938452/9RUxmLUV_OMKR5cdAgWGHoE3fuGnAagqiL9H52hOXtGFe19B65-vUAiR9om5sve4jmTt3ybX0mQ1UmUHVcjR5BfKpHqTMeL5y2tw.png",
  ]
  e = Embed(title="Prelude", colour=Colour.orange())
  e.set_image(url=choice(preludes))
  await ctx.send(
      embed=e,
      components=[
          create_actionrow(
              create_button(
                  style=ButtonStyle.blue,
                  label="Get Another",
                  custom_id="prelude_button",
              ))
      ],
  )


@slash.component_callback()
async def prelude_button(ctx: ComponentContext):
  preludes = [
      "https://cdn.discordapp.com/attachments/838805399162716190/848327737599852554/QFYOqx8AnHKJIHZliGeIBPeRaoO3i-YVUa_rF20bFPRkL3K1LxIwMSUYzb1KTcFNskppYuo8jyjOWmF9v8etKvIECuxSmOPzkj0r.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327840432521246/t7i6HA57SxRGezGs4oMEmcdmgW3zWfnSEHUPx7yPoQu-4Iq42NgPcr9I1Wv-fh-943ndC95pTbCF9EAViaUw_90mzP6pyFi7u3je.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327844081565727/akwkdGoC9KBq72dHxuq00wP4uL2ekOG-nQk9ssrXccP9MdkU6xoXsqBx6p0oxAxdWmDfWSHf8I5pY5GMKsudkl-b4GmVdkCucchm.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327845143248926/2G_ji_-QpvNSZnOWt1KS1kkX4AWmpxvVCEiJjIcy6GhyOLz9Sf9IO27_4ZBn4AmfzT9eLB7ckTYuP9KBzAHFjbNyRB6hUegFKrm9.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327891448365086/yr6Je-omEMbo_kVtwVRVrvEpwZBvYuezDfJnn2ji1Mh46lCP0Nu_pbYF4Q8ZvFzjeo6O7Jb999-7bcWIaW3lEHTzLMJZUciL5ID2.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848327891448365086/yr6Je-omEMbo_kVtwVRVrvEpwZBvYuezDfJnn2ji1Mh46lCP0Nu_pbYF4Q8ZvFzjeo6O7Jb999-7bcWIaW3lEHTzLMJZUciL5ID2.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328328699314186/r59rXgxtSVyelztQErzHInOCxIDwYcZrsTbUrmdVX6EpVAbXwErXui8L0EGNlGzhZgLxla9wsoBl7mqujfFIK_keVOUb_PQzzMbz.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328371489472562/fWOKrMMrJXPvQXSYr1UVmhCSuA3o5DlAP_ieZCRnOtUknizK411sWbCDLCF_RS8pwZZrJDr5zLTcTQ0G5YbtC0duvra7CGn7T0_a.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328415467929640/Eakx4kTtZZy32DHes7UzyTJEznVhgkDTDDXClsE4IVF6T7FyzBivmoh_Muoi9UsifvUwd4X_52vhz2SIFxS5fBLVmH3mqv5gLVxD.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328456122925086/mUA5X20Qo6omnrYSzTMRniZukZnMtltqoqp8mqKzqstwXG_VOE0iIPYCx2JT7ee_UDv3BxEsj3R-pvT4TRJbAdMajU8Wgg5YPu9z.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328557264764978/o8sa9VEaK1EJyVhcItTojizrw8OYglw05PDqCB84uj6uF2Ll9jlxEOie-AOpIoq9p9SR0WyixjWsOPKHTgV4xR4VHiHrmtxk0Um5.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328589777961021/-OEoGmagOx9osKooCw0udJyiqHmvwJxcQO-RVuhqViBxOI_orIDHMjubmlQDaxc68eL39Zt81iG_vu9BXkFKrVww6R9U58kVy-tc.png",
      "https://cdn.discordapp.com/attachments/838805399162716190/848328665137938452/9RUxmLUV_OMKR5cdAgWGHoE3fuGnAagqiL9H52hOXtGFe19B65-vUAiR9om5sve4jmTt3ybX0mQ1UmUHVcjR5BfKpHqTMeL5y2tw.png",
  ]
  e = Embed(title="Prelude", colour=Colour.orange(), footer=f"Requested by {ctx.origin_message.author.name}")
  e.set_image(url=choice(preludes))
  await ctx.send(
      embed=e,
      components=[
          create_actionrow(
              create_button(
                  style=ButtonStyle.blue,
                  label="Get Another",
                  custom_id="prelude_button",
              ))
      ],
  )

@slash.slash(
    name="snowflake",
    description="Get a picture of the cutest doggo ever.",
    guild_ids=guilds,
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def snowflake(ctx: SlashContext):
  snowflakes = [
      "https://cdn.discordapp.com/attachments/841542812104917014/879037764128112670/Screen_Shot_2021-03-11_at_1.03.57_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037765487054878/Screen_Shot_2021-03-11_at_1.11.42_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037765487054878/Screen_Shot_2021-03-11_at_1.11.42_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037806511534160/Screen_Shot_2021-03-24_at_9.13.36_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037810399645716/snowflake2.jpg",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037809724383302/SNOWFLAKE.jpg",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038794882494525/Screen_Shot_2021-08-22_at_9.24.32_AM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038803313061898/Screen_Shot_2021-08-22_at_9.24.42_AM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038803958960128/Screen_Shot_2021-08-22_at_9.24.56_AM.png"
  ]
  e = Embed(title="Snowflake", colour=Colour(0x82bbbe))
  e.set_image(url=choice(snowflakes))
  await ctx.send(
      embed=e,
      components=[
          create_actionrow(
              create_button(
                  style=ButtonStyle.blue,
                  label="Get Another",
                  custom_id="snowflake_button",
              ))
      ],
  )



@slash.component_callback()
async def snowflake_button(ctx: ComponentContext):
  snowflakes = [
      "https://cdn.discordapp.com/attachments/841542812104917014/879037764128112670/Screen_Shot_2021-03-11_at_1.03.57_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037765487054878/Screen_Shot_2021-03-11_at_1.11.42_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037765487054878/Screen_Shot_2021-03-11_at_1.11.42_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037806511534160/Screen_Shot_2021-03-24_at_9.13.36_PM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037810399645716/snowflake2.jpg",
      "https://cdn.discordapp.com/attachments/841542812104917014/879037809724383302/SNOWFLAKE.jpg",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038794882494525/Screen_Shot_2021-08-22_at_9.24.32_AM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038803313061898/Screen_Shot_2021-08-22_at_9.24.42_AM.png",
      "https://cdn.discordapp.com/attachments/841542812104917014/879038803958960128/Screen_Shot_2021-08-22_at_9.24.56_AM.png"
  ]
  e = Embed(title="Snowflake", colour=Colour(0x82bbbe))
  e.set_image(url=choice(snowflakes))
  await ctx.send(
      embed=e,
      components=[
          create_actionrow(
              create_button(
                  style=ButtonStyle.blue,
                  label="Get Another",
                  custom_id="snowflake_button",
              ))
      ],
  )


def remove_vote(name, vote, embed):
  index = list(map(lambda field: field["name"].startswith(name), embed["fields"])).index(True)

  embed["fields"][index]["value"] = "\n".join(list(filter(lambda e: e != vote, embed["fields"][index]["value"].split("\n"))))

  embed["fields"][index]["name"] = name + " (" + str(len(embed["fields"][index]["value"].split("\n"))) + ")" # adds to the wrong thing
  if embed["fields"][index]["value"] == "" or embed["fields"][index]["value"] == "No data yet.":
    embed["fields"][index]["name"] = name + " (0)"
    embed["fields"][index]["value"] = "No data yet."

  return embed

@bot.event
async def on_component(ctx: ComponentContext):
  if ctx.custom_id.startswith("suggestion_remove-"):
    try:
      message = await (await
                       bot.fetch_channel(847539091608043531)).fetch_message(
                           int(ctx.custom_id[18:]))
    except:
      await ctx.edit_origin(content="Suggestion already removed.")
      return
    await message.delete()
    await ctx.edit_origin(content="Suggestion removed.")
  elif ctx.custom_id.startswith("poll_remove-"):
    try:
      message = await (await
                       bot.fetch_channel(847539091608043531)).fetch_message(
                           int(ctx.custom_id[12:]))
    except:
      await ctx.edit_origin(content="Poll already removed.")
      return
    await message.delete()
    await ctx.edit_origin(content="Poll removed.")
  elif ctx.custom_id.startswith("stop_spam-"):
    jobs = schedule.get_jobs(ctx.custom_id[10:])
    if len(jobs) == 0:
      await ctx.edit_origin(content="Spam already stopped.")
      return
    schedule.clear(ctx.custom_id[10:])
    await ctx.edit_origin(content="Spam stopped.")
  elif ctx.custom_id.startswith("prop_remove-"):
    try:
      message = await (await
                       bot.fetch_channel(842631441220370452)).fetch_message(
                           int(ctx.custom_id[12:]))
    except:
      await ctx.edit_origin(content="Proposal already removed.")
      return
    await message.delete()
    await ctx.edit_origin(content="Proposal removed.")
  elif ctx.custom_id.startswith("event_remove-"):
    try:
      message = await (await
                       bot.fetch_channel(867982690031394827)).fetch_message(
                           int(ctx.custom_id[13:]))
    except:
      await ctx.edit_origin(content="Event already removed.")
      return
    await message.delete()
    await ctx.edit_origin(content="Event removed.")
  elif ctx.custom_id == "event_rsvp":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    index = list(map(lambda field: field["name"] == "Attendees", embed["fields"])).index(True)
    if ctx.author.mention in embed["fields"][index]["value"]:
      return
    if embed["fields"][index]["value"] == "No attendees yet.":
      embed["fields"][index]["value"] = "- " + ctx.author.mention
    else:
      embed["fields"][index]["value"] += "\n- " + ctx.author.mention
    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "event_unrsvp":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    index = list(map(lambda field: field["name"] == "Attendees", embed["fields"])).index(True)
    if ctx.author.mention not in embed["fields"][index]["value"]:
      return
    
    rsvp = "- " + ctx.author.mention
    embed["fields"][index]["value"] = "\n".join(list(filter(lambda e: e != rsvp, embed["fields"][index]["value"].split("\n"))))
    if embed["fields"][index]["value"] == "":
      embed["fields"][index]["value"] = "No attendees yet."
    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "upvote":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    embed = remove_vote("Downvoters", "- " + ctx.author.mention, embed)
    index = list(map(lambda field: field["name"].startswith("Upvoters"), embed["fields"])).index(True)

    if ctx.author.mention in embed["fields"][index]["value"]:
      return
    if embed["fields"][index]["value"] == "No data yet.":
      embed["fields"][index]["value"] = "- " + ctx.author.mention
    else:
      embed["fields"][index]["value"] += "\n- " + ctx.author.mention

    embed["fields"][index]["name"] = "Upvoters " + " (" + str(len(embed["fields"][index]["value"].split("\n"))) + ")"

    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "downvote":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    embed = remove_vote("Upvoters", "- " + ctx.author.mention, embed)
    index = list(map(lambda field: field["name"].startswith("Downvoters"), embed["fields"])).index(True)

    if ctx.author.mention in embed["fields"][index]["value"]:
      return
    if embed["fields"][index]["value"] == "No data yet.":
      embed["fields"][index]["value"] = "- " + ctx.author.mention
    else:
      embed["fields"][index]["value"] += "\n- " + ctx.author.mention

    embed["fields"][index]["name"] = "Downvoters " + " (" + str(len(embed["fields"][index]["value"].split("\n"))) + ")"

    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "clearvote":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    embed = remove_vote("Upvoters", "- " + ctx.author.mention, embed)
    embed = remove_vote("Downvoters", "- " + ctx.author.mention, embed)
    
    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "accept_application":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    if embed["fields"][list(map(lambda field: field["name"] == "Verified", embed["fields"])).index(True)]["value"] == "Yes":
      message = await ctx.send(ctx.author.mention + " tried to accept a member but failed to realize that the member was *already accepted*!")
      await message.add_reaction("👏")
      return

    firstname = embed["fields"][list(map(lambda field: field["name"] == "First Name", embed["fields"])).index(True)]["value"]
    lastname = embed["fields"][list(map(lambda field: field["name"] == "Last Name", embed["fields"])).index(True)]["value"]

    member = await ctx.guild.fetch_member(int("".join([letter for letter in embed["fields"][list(map(lambda field: field["name"] == "Member", embed["fields"])).index(True)]["value"] if letter.isdigit()])))

    await member.add_roles(ctx.guild.get_role(839941660942270464), reason="Verified")
    await member.edit(nick=firstname.capitalize() + " " + lastname[0].capitalize() + ".")
    
    e = Embed(
        title="Verified!",
        description="Thank you for verifying! You are now allowed to access the ICC Discord server. Please keep in mind your basic sense of morality while using the ICC Discord Server. Please also go to <#872667505246732320> to receive new roles including your grade level and so on. Additionally, if you would like to earn volunteer hours for any work done in the ICC, we encourage you to create a MyICC account for logging your volunteer hours. Please [create an account](https://irvinecodingclub.vercel.app/) and sign up. Then, navigate to your [dashboard](https://irvinecodingclub.vercel.app/dashboard) and click the \"edit membership\" button to fill in your credentials, including your school and grade. For membership, please simply write \"Member\". After completing these steps, you will be able to log PVSA certifying hours.\n\nWe hope you enjoy the ICC!",
        colour=15062910)
    await (await bot.fetch_channel(800120401107746849)).send(content=member.mention + " has been verified!", embed=e)

    embed["fields"][list(map(lambda field: field["name"] == "Verified", embed["fields"])).index(True)]["value"] = "Yes"

    await ctx.edit_origin(embed=Embed.from_dict(embed))
  elif ctx.custom_id == "deny_application":
    message = ctx.origin_message
    embed = message.embeds[0].to_dict()

    embed["fields"][list(map(lambda field: field["name"] == "Verified", embed["fields"])).index(True)]["value"] = "Denied (can always accept again, but go through approval from a president or vice president)"

    await ctx.edit_origin(embed=Embed.from_dict(embed))
  else:
    pass  # do stuff

def profane(text):
  return requests.get("https://www.purgomalum.com/service/containsprofanity?text=" + quote_plus(text)).text == "true"

@slash.slash(
    name="cuss",
    description="Hide your annoying profane messages.",
    guild_ids=guilds,
    options=[
        create_option(
            name="message",
            description="Your profane message goes here",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def cuss(ctx: SlashContext, message):
  bleeped = requests.get(
      "https://www.purgomalum.com/service/plain?fill_char=%3D&add=david&text=" +
      quote_plus(message)).text

  e = Embed(
      title="⚠️Cussing Alert⚠️",
      description="View the original message by hovering over the command.",
      colour=15783168)
  e.add_field(name="Bleeped Message", value=bleeped)
  e.add_field(name="Contains Profanity",
              value="No" if message == bleeped else "Yes")

  await ctx.send("Message sent by " + ctx.author.display_name, embed=e)


@slash.slash(
    name="suggest",
    description="Submit a suggestion.",
    guild_ids=guilds,
    options=[
        create_option(
            name="suggestion",
            description="Your wonderful idea",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def suggest(ctx: SlashContext, suggestion):
  e = Embed(title="Suggestion", description=suggestion, colour=15062910)
  e.add_field(name="Upvoters (0)", value="No data yet.")
  e.add_field(name="Downvoters (0)", value="No data yet.")
  e.add_field(name="Suggested By", value=ctx.author.mention)
  message = await (await bot.fetch_channel(847539091608043531)).send(embed=e, components=[
      create_actionrow(
          create_button(style=ButtonStyle(3),
                        label="Upvote",
                        custom_id="upvote")),
      create_actionrow(
          create_button(style=ButtonStyle(4),
                        label="Downvote",
                        custom_id="downvote")),
      create_actionrow(
          create_button(style=ButtonStyle(2),
                        label="Clear Vote",
                        custom_id="clearvote"))
  ])

  await ctx.send(
      embed=Embed(title="Success!",
                  description="This suggestion has been submitted."),
      components=[
          create_actionrow(
              create_button(style=ButtonStyle(4),
                            label="Remove Suggestion",
                            custom_id="suggestion_remove-" + str(message.id)))
      ],
      hidden=True)


def spam_ping(channel, embed, content, id):
  asyncio.create_task(
      channel.send(content,
                   embed=embed,
                   components=[
                       create_actionrow(
                           create_button(style=ButtonStyle(4),
                                         label="Stop the Spam",
                                         custom_id="stop_spam-" + id))
                   ]))


@slash.slash(
    name="spam",
    description="Spam ping a user with a threat.",
    guild_ids=guilds,
    options=[
        create_option(
            name="user",
            description="The person you want to annoy",
            option_type=6,
            required=True,
        ),
        create_option(
            name="reason",
            description="What you want the person to do",
            option_type=3,
            required=True,
        ),
        create_option(
            name="threat",
            description="A threat if they don't respond (ex: 'brain cell death')",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def spam(ctx: SlashContext, user, reason, threat):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to spam ping!", hidden=True)
  elif not user.guild_permissions.administrator:
    await ctx.send(
        "The user you are spam pinging must have admin to view your spam pinging!",
        hidden=True)
  else:
    name = user.display_name
    mention = user.mention
    embed = Embed.from_dict({
        "title":
        "Spam Ping for " + name,
        "description":
        ctx.author.display_name + " has requested a spam ping for " + name +
        "!",
        "fields": [{
            "name": "Reason",
            "value": reason,
            "inline": True
        }, {
            "name": "Threat",
            "value": threat,
            "inline": True
        }],
        "color":
        11745850
    })
    channel = await bot.fetch_channel(876538180206198794)

    spam_ping(channel=channel,
              embed=embed,
              content=mention,
              id=ctx.interaction_id)

    schedule.every(30).minutes.do(spam_ping,
                                  channel=channel,
                                  embed=embed,
                                  content=mention,
                                  id=ctx.interaction_id).tag(
                                      ctx.interaction_id)

    await ctx.send(
        embed=Embed(title="Success!",
                    description="This bot will now spam ping " +
                    escape(user.display_name) + "! For reason " +
                    escape(reason) + " with threat " + escape(threat) + "!"),
        components=[
            create_actionrow(
                create_button(style=ButtonStyle(4),
                              label="Stop Spamming " +
                              escape(user.display_name),
                              custom_id="stop_spam-" + ctx.interaction_id))
        ],
        hidden=True)


@slash.slash(
    name="nominate",
    description="Nominate a person for Member of the Month.",
    guild_ids=guilds,
    options=[
        create_option(
            name="member",
            description="Member to Nominate (mention)",
            option_type=6,
            required=True,
        ),
        create_option(
            name="reason",
            description="Reason to Nominate Member",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def nominate(ctx: SlashContext, member, reason):
  channel = None
  for _channel in ctx.guild.channels:
    if _channel.name == "member-of-the-month":
      channel = _channel
      break
  if channel == None:
    await ctx.send(
        "Must be a channel named member-of-the-month in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  messages = await channel.history(limit=1).flatten()
  if len(messages) == 0:
    await ctx.send(
        "Must have done /start_nominating to initiate the message before resetting nominations!",
        hidden=True)
    return
  message = (await channel.history(limit=1).flatten())[0]
  embed = message.embeds[0].to_dict()

  if "fields" not in embed:
    embed["fields"] = []

  tag = member.display_name
  fields = list(map(lambda e: e["name"] == tag, embed["fields"]))

  if len(list(filter(lambda e: e, fields))):
    embed["fields"][fields.index(True)]["value"] += "\n- " + escape(reason)
  else:
    embed["fields"].append({"name": tag, "value": "- " + escape(reason)})

  await message.edit(embed=Embed.from_dict(embed))
  await ctx.send(content="Nominated " + tag + " successfully!", hidden=True)


@slash.slash(
    name="reset_nominations",
    description="Reset nominations for this month and archive the results for judging.",
    guild_ids=guilds,
    options=[
        create_option(
            name="confirmation",
            description="Type 'CONFIRM_RESET' to confirm resetting this month's nominations (without quotes)",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def reset_nominations(ctx: SlashContext, confirmation):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to reset the nominations!",
                   hidden=True)
    return
  if confirmation != "CONFIRM_RESET":
    await ctx.send(
        "Wrong confirmation! Please type exactly 'CONFIRM_RESET' without the quotes!",
        hidden=True)
    return
  channel = None
  for _channel in ctx.guild.channels:
    if _channel.name == "member-of-the-month":
      channel = _channel
      break
  if channel == None:
    await ctx.send(
        "Must be a channel named member-of-the-month in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  messages = await channel.history(limit=1).flatten()
  if len(messages) == 0:
    await ctx.send(
        "Must have done /start_nominating to initiate the message before resetting nominations!",
        hidden=True)
    return
  message = messages[0]
  embed = message.embeds[0].to_dict()
  content = message.content

  nominations = None
  for _channel in ctx.guild.channels:
    if _channel.name == "nominations":
      nominations = _channel
      break
  if nominations == None:
    await ctx.send(
        "Must be a channel named nominations (to store nomination results) in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  await nominations.send(content=content, embed=Embed.from_dict(embed))

  await message.delete()

  new_embed = Embed(
      colour=15062910,
      description="You can now nominate anyone of your choosing (except for council members, please) with `/nominate member:<a mention of said member> reason:<what the member has done for the club over the month>`. Please note that this is a friendly competition. Do not bribe or harass to become the member of the month."
  )

  await channel.send("Member of the Month Nominations for " +
                     datetime.datetime.now().strftime("%B") + " 2021",
                     embed=new_embed)

  await ctx.send("Nominations reset successfully!", hidden=True)


@slash.slash(
    name="start_nominating",
    description="Start the member of the month nomination process.",
    guild_ids=guilds,
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def start_nominating(ctx: SlashContext):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send(
        "You must be an admin to start the member of the month process!",
        hidden=True)
    return
  channel = None
  for _channel in ctx.guild.channels:
    if _channel.name == "member-of-the-month":
      channel = _channel
      break
  if channel == None:
    await ctx.send(
        "Must be an empty channel named member-of-the-month in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  embed = Embed(
      colour=15062910,
      description="You can now nominate anyone of your choosing (except for council members, please) with `/nominate member:<a mention of said member> reason:<what the member has done for the club over the month>`. Please note that this is a friendly competition. Do not bribe or harass to become the member of the month."
  )

  await channel.send("Member of the Month Nominations for " +
                     datetime.datetime.now().strftime("%B") + " 2021",
                     embed=embed)

  await ctx.send("Nominations started successfully!", hidden=True)


@slash.slash(
    name="ship",
    description="Ship two people (as a joke, of course).",
    guild_ids=guilds,
    options=[
        create_option(
            name="person_1",
            description="First Person",
            option_type=3,
            required=True,
        ),
        create_option(
            name="person_2",
            description="Second Person",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def ship(ctx: SlashContext, person_1, person_2):
  parser = ship_parser.ShipParser()
  parser.feed(
      requests.post("https://www.name-generator.org.uk/add_creation.php",
                    data={
                        "type": 16,
                        "person_1_first_name": person_1,
                        "person_1_surname": "",
                        "person_2_first_name": person_2,
                        "person_2_surname": ""
                    }).text)

  embed = Embed(colour=16131713,
                title=person_1 + " x " + person_2,
                description="Requested by " + ctx.author.display_name +
                "\n\n**Ships:** " + ", ".join(parser.names[1:]))

  await ctx.send(embed=embed)


@slash.slash(
    name="help",
    description="Get some information about the Irvine Coding Club Bot.",
    guild_ids=guilds
)
async def help(ctx: SlashContext):
  await ctx.send(embed=Embed.from_dict({
      "title": "Irvine Coding Club Help",
      "description":
      "Welcome to the Irvine Coding Club Bot!\n\nOn this bot, you'll find plenty of fun commands. Here are some brief descriptions.\n - `/nominate` to nominate members for Member of the Month for their hard work.\n - `/suggest` to suggest an idea to the council.\n - `/ship` to generate a list of ship names for two people.\n - `/prelude` to get a picture of the cutest doggo ever!\n\nMore commands to be added!",
      "author": {
          "name": "Irvine Coding Club",
          "icon_url": "https://irvinecoding.club/assets/images/favicon.png"
      },
      "color": 15062910
  }),
                 hidden=True)


@slash.slash(
    name="info",
    description="Get important links to ICC resources.",
    guild_ids=guilds,
    options=[
        create_option(
            name="item",
            description="The item you want.",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="ICC Website", value="website_event"),
                create_choice(
                    name="ICC Join Link",
                    value="join_event"
                ),
                create_choice(name="ICC Facebook", value="facebook_event"),
                create_choice(name="ICC Instagram", value="instagram_event"),
                create_choice(name="ICC Youtube", value="youtube_event")
            ])
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def info(ctx: SlashContext, item):
  if item == "facebook_event":
    embed = {
        "title": "ICC Facebook",
        "description": "Click the button below to go to the ICC Facebook."
    }
    buttons = [
        create_actionrow(
            create_button(style=ButtonStyle(5),
                          label="ICC Facebook",
                          url="https://www.facebook.com/irvinecodingclub/"))
    ]

  elif item == "instagram_event":
    embed = {
        "title": "ICC Instagram",
        "description": "Click the button below to go to the ICC Instagram."
    }
    buttons = [
        create_actionrow(
            create_button(style=ButtonStyle(5),
                          label="ICC Instagram",
                          url="https://www.instagram.com/irvinecodingclub/"))
    ]

  elif item == "youtube_event":
    embed = {
        "title": "ICC Youtube Channel",
        "description":
        "Click the button below to go to the ICC Youtube channel."
    }
    buttons = [
        create_actionrow(
            create_button(
                style=ButtonStyle(5),
                label="ICC Youtube",
                url="https://www.youtube.com/channel/UCqN97rf-M3vnJq5g1IMZx4Q")
        )
    ]

  elif item == "website_event":
    embed = {
        "title": "ICC Website",
        "description": "Click the button below to go to the ICC website."
    }
    buttons = [
        create_actionrow(
            create_button(style=ButtonStyle(5),
                          label="ICC Youtube",
                          url="https://irvinecoding.club"))
    ]

  elif item == "join_event":
    embed = {
        "title": "ICC Join Link",
        "description": "Click the button below to get the link to join the ICC."
    }
    buttons = [
        create_actionrow(
            create_button(style=ButtonStyle(5),
                          label="ICC Join Link",
                          url="https://irvinecoding.club/join"))
    ]
  
  embed["color"] = 15062910

  await ctx.send(embed=Embed.from_dict(embed), components=buttons, hidden=True)


reactions = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]


@slash.slash(
    name="poll",
    description="Poll everyone.",
    guild_ids=guilds,
    options=[
        create_option(name="title",
                      description="Title of your poll",
                      option_type=3,
                      required=True),
        create_option(
            name="options",
            description="CSV of Options (ex. a,b,c); must not exceed 37 options (do not include commas in your poll options)",
            option_type=3,
            required=True)
    ],
    permissions={
      800120401107746846: [
        create_permission(839941660942270464, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def poll(ctx: SlashContext, title, options):
  options = options.split(",")

  if len(options) > 37:
    return ctx.send(
        "Sorry, your message had more than 37 options. If an option contains a comma, try to remove it.",
        hidden=True)

  channel = None
  for _channel in ctx.guild.channels:
    if _channel.name == "suggestions-n-polls":
      channel = _channel
      break
  if channel == None:
    await ctx.send(
        "Must be a channel named suggestions-n-polls in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return

  options = [{
      "name": "Option " + reactions[i],
      "value": escape(e.strip())
  } for i, e in enumerate(options)]

  embed = {"title": "Poll: " + title, "color": 15062910, "fields": options}

  message = await channel.send("Poll requested by " +
                               escape(ctx.author.display_name),
                               embed=Embed.from_dict(embed))

  for i in range(len(options)):
    await message.add_reaction(reactions[i])

  await ctx.send("Poll creation successful!\nView the message here: " +
                 message.jump_url,
                 hidden=True)


@slash.slash(
    name="purge",
    description="Purge the channel and wipe out messages.",
    guild_ids=guilds,
    options=[
        create_option(
            name="num",
            description="Number of messages to obliterate (leave blank to annihilate all messages in the channel)",
            option_type=4,
            required=False)
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def purge(ctx: SlashContext, num=None):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to purge channels!", hidden=True)
  if num == None:
    while await ctx.channel.purge(limit=100):
      ...
  elif num > 0:
    await ctx.channel.purge(limit=num)
  else:
    await ctx.send("Please purge a *positive integer*!", hidden=True)
    return
  await ctx.channel.send(("All" if num == None else str(num)) + " message" + ("s" if num != 1 else "") + " purged by " + ctx.author.display_name + "!")


@slash.slash(
    name="prop",
    description="Submit a proposal (for council members only).",
    guild_ids=guilds,
    options=[
        create_option(
            name="proposal",
            description="No profanity please.",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def prop(ctx: SlashContext, proposal):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to propose to the council!",
                   hidden=True)
    return

  propchannel = await bot.fetch_channel(879030521127133195)
  propnum = str(int((propchannel).name[20:]) + 1)

  await propchannel.edit(name="Proposition Number: " + propnum)

  e = Embed(title="Council Proposition #" + propnum, description=proposal, colour=15062910)
  e.add_field(name="Upvoters (0)", value="No data yet.")
  e.add_field(name="Downvoters (0)", value="No data yet.")
  e.add_field(name="Proposed By", value=ctx.author.mention)
  message = await (await bot.fetch_channel(842631441220370452)).send("@everyone", embed=e, components=[
          create_actionrow(
              create_button(style=ButtonStyle(3),
                            label="Upvote",
                            custom_id="upvote")),
          create_actionrow(
              create_button(style=ButtonStyle(4),
                            label="Downvote",
                            custom_id="downvote")),
          create_actionrow(
              create_button(style=ButtonStyle(2),
                            label="Clear Vote",
                            custom_id="clearvote"))
      ])

  await ctx.send(
      embed=Embed(title="Success!",
                  description="This proposal has been submitted."),
      components=[
          create_actionrow(
              create_button(style=ButtonStyle(4),
                            label="Remove Proposal",
                            custom_id="prop_remove-" + str(message.id)))
      ],
      hidden=True)


class SnipeStore:
    def __init__(self, channel):
        self.channel = channel
        self._messages = []
        pass
    
    def get(self, messages=1):
        return self._messages[:messages]
    
    def pop(self):
        if len(self._messages) == 0:
            return False
        return self._messages.pop()
    
    def add(self, message):
        return self._messages.append(message)

async def attachment_to_file(attachment):
    return File(fp=io.BytesIO(await attachment.read()), filename=attachment.filename) # for snipe
    # but reusable

class SnipedMessage:
    @classmethod
    async def create(cls, created_at, deleted_at, author, deleter, content, embeds, attachments):
        self = SnipedMessage()
        self.created_at = created_at.strftime("%m/%d/%Y, %H:%M:%S")
        self.deleted_at = deleted_at.strftime("%m/%d/%Y, %H:%M:%S")
        self.author = author.mention
        self.deleter = deleter
        self.content = content
        self.embeds = embeds
        self.files = [await attachment_to_file(i) for i in attachments]
        return self

snipes = {}
@slash.slash(
    name="snipe",
    description="Reveal the last message deleted in the channel",
    guild_ids=guilds,
    options=[
        create_option(
            name="channel",
            description="No profanity please.",
            option_type=7,
            required=False,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def snipe(ctx: SlashContext, channel=None):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to snipe messages!",
                  hidden=True)
    return

  if channel == None:
    channel = ctx.channel
  elif channel.type in [ChannelType.text, ChannelType.news]:
    await ctx.send(content="Error: channel was not a text channel.")
    return
  
  if channel.id not in snipes:
    snipes[channel.id] = SnipeStore(channel.id)
  
  messages = snipes[channel.id].get()
  if len(messages) == 0:
    await ctx.send(content="No messages to snipe in " + channel.mention + "!", hidden=True)
    return  
  snipes[channel.id].pop()

  message = messages[0]

  embed = Embed(title="Snipe Requested by " + ctx.author.display_name,
                  description="Actual message below.")

  embed.add_field(name="Sent By", value=message.author)
  embed.add_field(name="Deleted By", value=message.deleter)
  embed.add_field(name="Created At", value=message.created_at, inline=False)
  embed.add_field(name="Deleted At", value=message.deleted_at, inline=False)

  await ctx.send(embed=embed)

  if len(message.content) != 0 or len(message.files) != 0:
    await ctx.channel.send(content=message.content, files=message.files)

  for i, embed in enumerate(message.embeds):
    await ctx.channel.send(content="Embed #" + str(i), embed=Embed.from_dict(embed.to_dict()))

@bot.event
async def on_message_delete(message):
  deleter = message.author.mention
  async for entry in message.guild.audit_logs(limit=1,action=AuditLogAction.message_delete):
    if entry.extra.channel.id == message.channel.id:
      deleter = entry.user.mention
    else:
      deleter = "Unknown"

  if message.channel.id not in snipes:
    snipes[message.channel.id] = SnipeStore(message.channel.id)
  
  snipes[message.channel.id].add(await SnipedMessage.create(created_at=message.created_at, deleted_at=datetime.datetime.now(), author=message.author, deleter=deleter, content=message.content, embeds=message.embeds, attachments=message.attachments))


@bot.event
async def on_message(message):
  return
  if message.author.guild_permissions.administrator and message.author.id != 738900809810575390: # admin
    return

  if profane(message.content): # also check like embeds and stuff
    await message.delete()
    return


  # to_check = []
  # for attachment in message.attachments:
  #   stuff = io.BytesIO(await attachment.read())
  #   stuff.seek(0)
  #   with open("attachment_cache/" + attachment.filename, "wb") as f:
  #     shutil.copyfileobj(stuff, f, length=131072)
  #   to_check.append("attachment_cache/" + attachment.filename)
  #   for image in to_check:
  #     img = cv2.imread(image)
  #     if profane(pytesseract.image_to_string(img)): 
  #       await message.delete()
  #       message.channel.send(message.author.mention + " has sent a profane message.")
  #       return



  
    


url_test = re.compile("^https?:\/\/docs\.google\.com\/document\/d\/[0-9a-zA-Z-]+\/edit(\?usp=sharing)?(#.*)?$")
@slash.slash(
    name="event",
    description="Create an event for the ICC.",
    guild_ids=guilds,
    options=[
        create_option(
            name="title",
            description="Title of your event (ex: 'Activity at Place on Date')",
            option_type=3,
            required=True,
        ),
        create_option(
            name="who",
            description="Who is needed at this event? Include approximately how many people should attend and their jobs.",
            option_type=3,
            required=True,
        ),
        create_option(
            name="what",
            description="What will happen at this event? Include your goal(s), estimated expenses, and any equipment needed.",
            option_type=3,
            required=True,
        ),
        create_option(
            name="where",
            description="Where will this event take place? Include any permits needed and any site hazards or weather issues.",
            option_type=3,
            required=True,
        ),
        create_option(
            name="location",
            description="What is the location? Include the location, directions, and how to arrive. ('Virtual' is an option).",
            option_type=3,
            required=True,
        ),
        create_option(
            name="when",
            description="When will this event take place? Include a date and time as well as the times for shifts.",
            option_type=3,
            required=True,
        ),
        create_option(
            name="how",
            description="What still needs to be done? Include steps and deadlines, and who should do it (ex: 'ICC Artist').",
            option_type=3,
            required=True,
        ),
        create_option(
            name="doc",
            description="A Google Document with more information and a table to sign up for shifts and to bring materials.",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def event(ctx: SlashContext, title, who, what, where, location, when, how, doc):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to create events!",
                  hidden=True)
    return
  
  if not url_test.fullmatch(doc):
    await ctx.send("Your document must be a link in the form of a Google Document!",
                  hidden=True)
    return

  e = Embed(title=title, description=ctx.author.mention + " has created an event! Please RSVP (by clicking the green button at the bottom) as you will receive volunteer hours for your hard work as well as support the Irvine Coding Club.", colour=15062910)
  e.add_field(name="Who", value=who)
  e.add_field(name="What", value=what)
  e.add_field(name="Where", value=where)
  e.add_field(name="Location", value=location)
  e.add_field(name="When", value=when)
  e.add_field(name="How", value=how)
  e.add_field(name="Document (with more info)", value=doc)
  e.add_field(name="Attendees", value="No attendees yet.")

  channel = await bot.fetch_channel(881704635226812426)
  message = await channel.send(embed=e, components=[
          create_actionrow(
              create_button(style=ButtonStyle(3),
                            label="RSVP",
                            custom_id="event_rsvp"),
              create_button(style=ButtonStyle(4),
                            label="UnRSVP",
                            custom_id="event_unrsvp"))
      ])

  await ctx.send(
      embed=Embed(title="Success!",
                  description="This event has been created."),
      components=[
          create_actionrow(
              create_button(style=ButtonStyle(4),
                            label="Remove Event",
                            custom_id="event_remove-" + str(message.id)))
      ],
      hidden=True)

@bot.event
async def on_reaction_remove(reaction, member):
  message = reaction.message
  channel = message.guild.get_channel(847204787023118366)
  embed=Embed(title="Reaction was removed.", description=member.mention + " removed a reaction.", colour=15062910)
  embed.add_field(name="Channel", value=message.channel.mention)
  embed.add_field(name="Message", value=message.jump_url)
  embed.add_field(name="Emoji", value=str(reaction))
  await channel.send(embed=embed)

pages = ["**0. Introduction**\n\nPlease read the entirety of these Terms and Conditions thoroughly because it explains your rights and responsibilities while accessing the Irvine Coding Club Discord server. By accepting these Terms, **you agree to be bound by these Terms and held accountable for violating these terms**. The Irvine Coding Club may take measures to prevent future violations of the Terms by kicking or banning any member at any time. The Irvine Coding Club reserves the right to update these terms at any time.", "**1. Acceptable Use**\n\nTo:\n- Engage or promote anything illegal or otherwise violate applicable law, Threaten, harass, or violate the privacy rights of others, Harm users with malicious code or instructions, in attacks not limited to, viruses, malware, or trojan horses, Deceive, mislead, defraud, phish, or attempt to commit identity theft, Violate the privacy rights of others, Collect or harvest personally identifiable information without permission which includes, but is not limited to, account names and email addresses, Engage in any activity that interferes with or disrupts the services provided.\n- Engage or promote anything illegal or otherwise violate applicable law,\n- Threaten, harass, or violate the privacy rights of others,\n- Harm users with malicious code or instructions, in attacks not limited to, viruses, malware, or trojan horses,\n- Deceive, mislead, defraud, phish, or attempt to commit identity theft,\n- Violate the privacy rights of others,\n- Collect or harvest personally identifiable information without permission which includes, but is not limited to, account names and email addresses,\n- Engage in any activity that interferes with or disrupts the services provided.\n\nis prohibited on the Irvine Coding Club Discord server.\n\n**Note:** this is not an exhaustive list and any moderator may choose to add any rule whenever. You will still be required to follow any new updated rules.", "**2. Server Rules**\n\n1) Be respectful.  This is self explanatory. Don't be rude. This includes any discrimination of any kind -- including about coding skills. Avoid spam and all caps without reason, and try to be respectful. Please keep profanity to a minimum.\n2) Please use /verify and enter your real name and school when you join.\n3) Have fun!  It's a club! Code! Talk! Make friends! Collaborate!"]

@slash.slash(
    name="TOC",
    description="Terms and Conditions for the ICC.",
    guild_ids=test_guilds
)
async def TOC(ctx: SlashContext):
  e = Embed(
        title="Page 0 / " + str(len(pages) - 1), 
        description=pages[0],
        colour=15062910)
  await ctx.send("ICC Terms and Conditions", embed=e, components=[
      create_actionrow(
          create_button(style=ButtonStyle(2),
                        label="Previous Page",
                        custom_id="TOC_prev_page"),
          create_button(style=ButtonStyle(2),
                        label="Next Page",
                        custom_id="TOC_next_page"),
          create_button(style=ButtonStyle(3),
                        label="Accept Terms and Conditions",
                        custom_id="TOC_accept"))
  ])


@slash.component_callback()
async def TOC_next_page(ctx: ComponentContext):
  page = int(ctx.origin_message.embeds[0].title[5:].split("/")[0][:-1]) + 1
  if page == len(pages):
    await ctx.send(content="You are already at the last page and can not move forwards!", hidden=True)
    return
  content = pages[page]

  e = ctx.origin_message.embeds[0].to_dict()
  e["title"] = "Page " + str(page) + " / " + str(len(pages) - 1)
  e["description"] = content

  await ctx.edit_origin(embed=Embed.from_dict(e))


@slash.component_callback()
async def TOC_prev_page(ctx: ComponentContext):
  page = int(ctx.origin_message.embeds[0].title[5:].split("/")[0][:-1]) - 1
  if page == -1:
    await ctx.send(content="You are already at the first page and can not move backwards!", hidden=True)
    return
  content = pages[page]

  e = ctx.origin_message.embeds[0].to_dict()
  e["title"] = "Page " + str(page) + " / " + str(len(pages) - 1)
  e["description"] = content

  await ctx.edit_origin(embed=Embed.from_dict(e))


@slash.component_callback()
async def TOC_accept(ctx: ComponentContext):
  page = int(ctx.origin_message.embeds[0].title[5:].split("/")[0][:-1])
  if page != len(pages) - 1:
    await ctx.send(content="Please read the entirety of the Terms and Conditions before agreeing! (It isn't long).", hidden=True)
    return
  
  await ctx.send("You have accepted the Terms and Conditions!")
  # accept TOC

  # perhaps include the ID of the message (from the icc-logs) in this component thing and move it way up


@slash.slash(
    name="form",
    description="Create a form for the council to fill out.",
    guild_ids=test_guilds,
    options=[
        create_option(
            name="link",
            description="Form link",
            option_type=3,
            required=True,
        )
    ],
    permissions={
      800120401107746846: [
        create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
        create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
        create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
      ]
    }
)
async def form(ctx: SlashContext, link):
  if not ctx.author.guild_permissions.administrator:
    await ctx.send("You must be an admin to create forms!",
                  hidden=True)
    return
  
  channel = None
  for _channel in ctx.guild.channels:
    if _channel.name == "council-alerts":
      channel = _channel
      break
  if channel == None:
    await ctx.send(
        "Must be a channel named council-alerts in the server you are using this command! Please contact an admin if you believe this is a mistake!",
        hidden=True)
    return
  
  # send embed (description = 
  """
  Fill out [this form](" + link + ").\n\nIf you do not fill out this form, or lie and say that you have filled out this form without having actually having succeeded in your duty, punishments will be required. By reading this message, you agree to these terms. 
  """
  #)
  # ping everyone
  # add them to people who have finished once they press button
  # ping person who created, once everyone has filled out
  # (do this by doing a list of people who still need to be filled out, kind of like people who up voted then downvoted, the upvoted is still need to be filled out)
  # can't say you have not finished once you have already pressed button



# @slash.slash(
#     name="unrsvp",
#     description="UnRSVP a person if they are experiencing issues.",
#     guild_ids=guilds,
#     options=[
#         create_option(
#             name="message",
#             description="Message ID or Message Link",
#             option_type=3,
#             required=True,
#         ),
#         create_option(
#             name="member",
#             description="Member to unRSVP.",
#             option_type=6,
#             required=True,
#         )
#     ],
#     permissions={
#       800120401107746846: [
#         create_permission(800157008975364106, SlashCommandPermissionType.ROLE, True),
#         create_permission(808208118144172042, SlashCommandPermissionType.ROLE, True),
#         create_permission(816391279650275388, SlashCommandPermissionType.ROLE, True)
#       ]
#     }
# )
# async def unrsvp(ctx: SlashContext, message, member):
#   if not ctx.author.guild_permissions.administrator:
#     await ctx.send("You must be an admin to unRSVP people!",
#                   hidden=True)
#     return

  
#   message_id = message.split("/")[-1]
#   if not message_id.isdigit():
#     await ctx.send("Invalid message link or ID.",
#                   hidden=True)
#     return

#   channel = await bot.fetch_channel(867982690031394827)
#   try:
#     message = await channel.fetch_message(message_id)
#   except:
#     await ctx.send("Invalid message link or ID.",
#                   hidden=True)
#     return

#   embed = message.embeds[0].to_dict()
#   try:
#     index = list(map(lambda field: field["name"] == "Attendees", embed["fields"])).index(True)
#   except:
#     await ctx.send("Invalid message link or ID.",
#                   hidden=True)
#     return

#   if member.mention not in embed["fields"][index]["value"]:
#     await ctx.send("Member was not found in attendee list.",
#                   hidden=True)
#     return
  
#   rsvp = "- " + member.mention
#   embed["fields"][index]["value"] = "\n".join(list(filter(lambda e: e != rsvp, embed["fields"][index]["value"].split("\n"))))
#   if embed["fields"][index]["value"] == "":
#     embed["fields"][index]["value"] = "No attendees yet."
#   await message.edit(embed=Embed.from_dict(embed))

#   await ctx.send("UnRSVPed " + member.display_name + " successfully!",
#                   hidden=True)
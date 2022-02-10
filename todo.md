# Todo

### Commands
- on_member_join
  - automatically add them to Unverified role
  - create a new channel (in a new category named Unverified) and https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.set_permissions allow them to send messages
  - do an embed
    - title: Welcome to the Irvine Coding Club!
    - description: Please type `/verify` to get access to the channels in this server. If you experience any issues, feel free to DM any admin to ask for help.
    - thumbnail/image: https://irvinecoding.club/assets/images/mission.png
    ![test](https://irvinecoding.club/assets/images/poster.jpg)
  - once they `/verify`, do the terms of service
    - this involves: creating embed and pages
    - components: next_page (gets the current pages and set content to next page, check if it is already the last page), prev_page (same thing basically, check if it is already the first page), accept (check if pages is the last one, and then, edit the application thing in icc-logs by saying that they accepted TOC)
  - additionally, in the beginning application thing, do a link to the channel
  - when trying to accept an application, check if accepted TOC, and if not, do 
  ```python
  await ctx.send("The user you are trying to accept has not yet accepted the Terms and Conditions. Please wait to verify until they do.")
  ur mom
  david good
  ```

# do /voting-form
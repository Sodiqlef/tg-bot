from secretkey import TELEGRAM_BOT_TOKEN
import aiohttp
import os
from telegram.ext import Application, CommandHandler

TOKEN = TELEGRAM_BOT_TOKEN
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/solana/contract/"

async def start(update, context):
    #/start comand output
    welcome_message = (
        "🌟 Hello! Welcome to the GoldenBoysAlertBot 🌟\n\n"
        "I’m your Solana Token Bot 🤖 fetching real-time token details like name and market cap from CoinGecko 📊.\n\n"
        "Drop a /alert <ca> to see me shine ✨. \n\nTry it with EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v (USDC) for a taste! 🍬\n\n"
        "Let’s blast off into the Solana universe! 🚀🌌"
    )
    await update.message.reply_text(welcome_message)

async def alert(update, context):
    # /alert token info from coingecko
    if update.message.chat.type in ['group', 'supergroup']:  
        if context.args: 
            solana_address = context.args[0]  
            
            # Fetch token name, market cap, price, description, and image from CoinGecko
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{COINGECKO_API_URL}{solana_address}") as response:
                        if response.status == 200:
                            data = await response.json()
                            token_name = data.get("name", "Unknown Token")
                            market_cap = data.get("market_data", {}).get("market_cap", {}).get("usd", "N/A")
                            description = data.get("description", "").get("en", "No description")
                            price = data.get("market_data", {}).get("current_price", {}).get("usd", "N/A")
                            image_url = data.get("image", {}).get("large", None)  # Get the large image URL
                            
                            if market_cap != "N/A":
                                market_cap = f"${market_cap:,.2f}"
                            if price != "N/A":
                                price = f"${price:,.2f}"

                            # Prepare the text message
                            text_message = (
                                f"📍 *Address:* _{solana_address}_\n"
                                f"🏷️ *Token Name:* {token_name}\n"
                                f"💰 *Price:* {price}\n"
                                f"📈 *Market Cap:* {market_cap}\n\n"
                                f"📝 *Description:* _{description}_\n"
                            )

                            # Send the image if available, followed by the text
                            if image_url:
                                await context.bot.send_photo(
                                    chat_id=update.message.chat_id,
                                    photo=image_url,
                                    caption=text_message,
                                    parse_mode = "Markdown"
                                )
                            else:
                                await context.bot.send_message(
                                    chat_id=update.message.chat_id,
                                    text=text_message + "\n(No image available)",
                                    parse_mode = "Markdown"
                                )
                        else:
                            await context.bot.send_message(
                                chat_id=update.message.chat_id,
                                text=(
                                    f"📢 ALERT: Solana Token - {solana_address}\n"
                                    "Token Name: Not found on CoinGecko\n"
                                    "Market Cap: Not available"
                                )
                            )
            except Exception as e:
                await update.message.reply_text(
                    f"Error fetching token data for {solana_address}: {str(e)}"
                )
        else:
            await update.message.reply_text(
                "Please provide a Solana token address with /alert, e.g., /alert EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            )
    else:
        await update.message.reply_text("This command only works in groups!")
def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("alert", alert))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
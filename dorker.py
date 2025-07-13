import os
import time
import requests
from ddgs import DDGS
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import asyncio
import logging
import json
import hashlib
from datetime import datetime
import random

# 🎨 Futuristic Color Schemes & Emojis
CYBER_EMOJIS = {
    'search': '🔍',
    'cyber': '🌐',
    'rocket': '🚀',
    'lightning': '⚡',
    'shield': '🛡️',
    'diamond': '💎',
    'fire': '🔥',
    'star': '⭐',
    'robot': '🤖',
    'gear': '⚙️',
    'target': '🎯',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'loading': '🔄',
    'data': '📊',
    'scan': '🔬',
    'hack': '💻',
    'secure': '🔐',
    'neural': '🧠',
    'quantum': '⚛️',
    'matrix': '📱',
    'signal': '📡',
    'pulse': '💫'
}

# 🎯 Advanced logging with futuristic formatting
logging.basicConfig(
    format='%(asctime)s - [🤖 NEXUS] - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEVELOPER_TAG = "@knowlay"

# 🚀 Neural Network Style Banner
NEXUS_BANNER = f"""
╔══════════════════════════════════════╗
║  🌐 NEXUS SEARCH ENGINE v2.0 🌐       ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  {CYBER_EMOJIS['quantum']} Quantum Search Technology      ║
║  {CYBER_EMOJIS['neural']} Neural Network Powered         ║
║  {CYBER_EMOJIS['lightning']} Lightning Fast Results       ║
║  {CYBER_EMOJIS['shield']} Secure & Anonymous             ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  🔧 Developed by: {DEVELOPER_TAG}           ║
╚══════════════════════════════════════╝
"""

# 🎨 Advanced UI Components
def create_progress_bar(percentage, width=20):
    """Create a futuristic progress bar"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percentage}%"

def create_cyber_divider():
    """Create a cyberpunk-style divider"""
    return "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

def format_search_stats(total_results, search_time, sources):
    """Format search statistics in a futuristic way"""
    return f"""
{CYBER_EMOJIS['data']} **NEURAL ANALYSIS COMPLETE**
{create_cyber_divider()}
{CYBER_EMOJIS['target']} **Results Found:** `{total_results}`
{CYBER_EMOJIS['lightning']} **Processing Time:** `{search_time:.2f}s`
{CYBER_EMOJIS['signal']} **Sources Scanned:** `{', '.join(sources)}`
{CYBER_EMOJIS['quantum']} **Quantum Accuracy:** `99.7%`
{create_cyber_divider()}
"""

def create_futuristic_keyboard():
    """Create a futuristic inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(f"{CYBER_EMOJIS['search']} Quick Search", callback_data="quick_search"),
            InlineKeyboardButton(f"{CYBER_EMOJIS['gear']} Advanced", callback_data="advanced_search")
        ],
        [
            InlineKeyboardButton(f"{CYBER_EMOJIS['data']} Analytics", callback_data="analytics"),
            InlineKeyboardButton(f"{CYBER_EMOJIS['shield']} Security", callback_data="security")
        ],
        [
            InlineKeyboardButton(f"{CYBER_EMOJIS['neural']} Neural Mode", callback_data="neural_mode"),
            InlineKeyboardButton(f"{CYBER_EMOJIS['quantum']} Quantum Boost", callback_data="quantum_boost")
        ],
        [
            InlineKeyboardButton(f"{CYBER_EMOJIS['hack']} Developer: {DEVELOPER_TAG}", url="https://t.me/knowlay")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def serpapi_quantum_search(dork, num_results, api_key):
    """🚀 Quantum-enhanced SerpAPI search with neural processing"""
    results = []
    retries = 3
    start = 0
    
    if not api_key:
        logger.error(f"{CYBER_EMOJIS['error']} SERPAPI_KEY neural link not established")
        return results
    
    while len(results) < num_results and retries > 0:
        try:
            # 🌐 Quantum parameter optimization
            params = {
                'q': dork,
                'num': min(num_results - len(results), 10),
                'api_key': api_key,
                'engine': 'google',
                'start': start,
                'gl': 'us',  # Geolocation
                'hl': 'en'   # Language
            }
            
            logger.info(f"{CYBER_EMOJIS['loading']} Quantum tunneling through SerpAPI matrix...")
            response = requests.get('https://serpapi.com/search', params=params, timeout=15)
            
            if response.status_code == 429:
                logger.warning(f"{CYBER_EMOJIS['warning']} Neural overload detected - initiating cooldown protocol")
                retries -= 1
                await asyncio.sleep(5)
                continue
            elif response.status_code == 401:
                logger.error(f"{CYBER_EMOJIS['error']} Authentication matrix breached - check neural key")
                break
            elif response.status_code != 200:
                logger.error(f"{CYBER_EMOJIS['error']} Quantum interference detected: {response.status_code}")
                break

            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                logger.error(f"{CYBER_EMOJIS['error']} Neural network error: {data['error']}")
                break
                
            organic_results = data.get('organic_results', [])
            if not organic_results:
                logger.info(f"{CYBER_EMOJIS['signal']} Quantum scan complete - no more data streams")
                break
                
            for result in organic_results:
                link = result.get('link')
                if link and len(results) < num_results:
                    results.append(link)
                    
            start += len(organic_results)
            await asyncio.sleep(1)  # Neural processing delay
            
        except Exception as e:
            logger.error(f"{CYBER_EMOJIS['error']} Quantum disruption: {e}")
            retries -= 1
            if retries > 0:
                await asyncio.sleep(2)
            
    return results

async def duckduckgo_neural_search(dork, num_results):
    """🧠 Neural-enhanced DuckDuckGo search"""
    results = []
    try:
        logger.info(f"{CYBER_EMOJIS['neural']} Activating DuckDuckGo neural interface...")
        with DDGS() as ddgs:
            search_results = ddgs.text(dork, max_results=num_results)
            for r in search_results:
                url = r.get('href')
                if url:
                    results.append(url)
                    if len(results) >= num_results:
                        break
                await asyncio.sleep(0.3)  # Neural processing delay
    except Exception as e:
        logger.error(f"{CYBER_EMOJIS['error']} Neural network disruption: {e}")
    return results

async def perform_quantum_search(dork: str, max_urls: int):
    """🚀 Quantum-powered multi-source search"""
    start_time = time.time()
    
    if max_urls < 1:
        return [], 0, []

    # 🎯 Quantum resource allocation
    serpapi_count = max(1, int(max_urls * 0.7)) if SERPAPI_KEY else 0
    ddg_count = max_urls - serpapi_count
    sources = []

    all_urls = []

    # 🌐 SerpAPI Quantum Search
    if serpapi_count > 0 and SERPAPI_KEY:
        logger.info(f"{CYBER_EMOJIS['quantum']} Initiating SerpAPI quantum search...")
        serpapi_results = await serpapi_quantum_search(dork, serpapi_count, SERPAPI_KEY)
        all_urls.extend(serpapi_results)
        sources.append("SerpAPI")

    # 🧠 DuckDuckGo Neural Search
    if ddg_count > 0:
        logger.info(f"{CYBER_EMOJIS['neural']} Activating DuckDuckGo neural search...")
        ddg_results = await duckduckgo_neural_search(dork, ddg_count)
        all_urls.extend(ddg_results)
        sources.append("DuckDuckGo")

    # 🔬 Quantum deduplication
    seen = set()
    unique_urls = []
    for url in all_urls:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        if url_hash not in seen:
            seen.add(url_hash)
            unique_urls.append(url)

    trimmed_urls = unique_urls[:max_urls]
    search_time = time.time() - start_time

    # 💾 Neural data storage (JSON logs)
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("nexus_search_logs.json", "a", encoding="utf-8") as f:
            search_data = {
                "timestamp": timestamp,
                "dork": dork,
                "results_count": len(trimmed_urls),
                "search_time": search_time,
                "sources": sources,
                "results": trimmed_urls
            }
            f.write(json.dumps(search_data) + "\n")
    except Exception as e:
        logger.error(f"{CYBER_EMOJIS['error']} Neural storage error: {e}")

    # 📄 Generate futuristic result.txt file
    try:
        result_filename = f"nexus_results_{int(time.time())}.txt"
        with open(result_filename, "w", encoding="utf-8") as f:
            # Futuristic header
            f.write("╔══════════════════════════════════════════════════════════════╗\n")
            f.write("║                    🌐 NEXUS SEARCH RESULTS 🌐                 ║\n")
            f.write("║                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║\n")
            f.write("║                    Quantum Search Technology v2.0             ║\n")
            f.write("╚══════════════════════════════════════════════════════════════╝\n\n")
            
            # Search metadata
            f.write("🔍 SEARCH PARAMETERS:\n")
            f.write(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write(f"🎯 Query: {dork}\n")
            f.write(f"📊 Results Found: {len(trimmed_urls)}\n")
            f.write(f"⚡ Processing Time: {search_time:.2f} seconds\n")
            f.write(f"🌐 Sources: {', '.join(sources)}\n")
            f.write(f"🕐 Timestamp: {timestamp}\n")
            f.write(f"🤖 Generated by: NEXUS Bot (@knowlay)\n")
            f.write(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
            
            # Results section
            f.write("🔗 QUANTUM SEARCH RESULTS:\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            
            for url in trimmed_urls:
                f.write(f"{url}\n")
            
            f.write("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write("🚀 END OF QUANTUM RESULTS\n")
            f.write("🔧 Developed by: @knowlay\n")
            f.write("💎 NEXUS Search Engine v2.0\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            
    except Exception as e:
        logger.error(f"{CYBER_EMOJIS['error']} Result file generation error: {e}")
        result_filename = None

    return trimmed_urls, search_time, sources, result_filename

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🔍 Advanced quantum search command"""
    if not update.message:
        return
        
    if not context.args or len(context.args) < 2:
        help_text = f"""
{CYBER_EMOJIS['robot']} **NEXUS SEARCH PROTOCOL**
{create_cyber_divider()}
{CYBER_EMOJIS['lightning']} **Usage:** `/search <dork> <max_urls>`
{CYBER_EMOJIS['target']} **Example:** `/search inurl:admin 25`
{CYBER_EMOJIS['neural']} **Advanced:** `/search "site:example.com filetype:pdf" 50`
{create_cyber_divider()}
{CYBER_EMOJIS['quantum']} **Quantum Limits:** 1-200 results
{CYBER_EMOJIS['shield']} **Neural Protection:** Enabled
{CYBER_EMOJIS['fire']} **Developer:** {DEVELOPER_TAG}
        """
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    try:
        dork = " ".join(context.args[:-1])
        max_urls = int(context.args[-1])
        
        if max_urls < 1:
            await update.message.reply_text(f"{CYBER_EMOJIS['error']} **Neural Error:** Minimum 1 result required")
            return
            
        if max_urls > 200:
            await update.message.reply_text(f"{CYBER_EMOJIS['warning']} **Quantum Limit:** Maximum 200 results to prevent neural overload")
            return
            
    except ValueError:
        await update.message.reply_text(f"{CYBER_EMOJIS['error']} **Parse Error:** Invalid quantum parameter")
        return

    # 🚀 Initiate quantum search sequence
    init_message = f"""
{CYBER_EMOJIS['rocket']} **NEXUS QUANTUM SEARCH INITIATED**
{create_cyber_divider()}
{CYBER_EMOJIS['scan']} **Target:** `{dork}`
{CYBER_EMOJIS['data']} **Quantum Limit:** `{max_urls} results`
{CYBER_EMOJIS['loading']} **Status:** Neural networks activating...
{create_cyber_divider()}
{CYBER_EMOJIS['pulse']} **Processing...**
    """
    
    status_message = await update.message.reply_text(init_message, parse_mode="Markdown")

    try:
        # 🔬 Quantum search execution
        results, search_time, sources, result_filename = await perform_quantum_search(dork, max_urls)

        if not results:
            failure_message = f"""
{CYBER_EMOJIS['error']} **QUANTUM SEARCH FAILED**
{create_cyber_divider()}
{CYBER_EMOJIS['signal']} **Result:** No data streams detected
{CYBER_EMOJIS['neural']} **Suggestion:** Try different neural parameters
{CYBER_EMOJIS['hack']} **Developer:** {DEVELOPER_TAG}
            """
            await status_message.edit_text(failure_message, parse_mode="Markdown")
            return

        # 📊 Success report
        success_stats = format_search_stats(len(results), search_time, sources)
        await status_message.edit_text(success_stats, parse_mode="Markdown")

        # 🎯 Results delivery with quantum formatting
        result_header = f"""
{CYBER_EMOJIS['success']} **QUANTUM RESULTS ACQUIRED**
{create_cyber_divider()}
{CYBER_EMOJIS['diamond']} **Neural Analysis:** {len(results)} URLs extracted
{CYBER_EMOJIS['fire']} **Quantum Query:** `{dork}`
{create_cyber_divider()}
        """

        # 📱 Chunk results for optimal delivery
        max_chunk_size = 3800
        result_text = result_header + "\n".join(f"{CYBER_EMOJIS['matrix']} `{url}`" for url in results)
        
        if len(result_text) <= max_chunk_size:
            await update.message.reply_text(result_text, parse_mode="Markdown")
        else:
            # Send header first
            await update.message.reply_text(result_header, parse_mode="Markdown")
            
            # Send results in chunks
            chunk_size = 3500
            for i in range(0, len(results), 20):  # 20 URLs per chunk
                chunk = results[i:i+20]
                chunk_text = "\n".join(f"{CYBER_EMOJIS['matrix']} `{url}`" for url in chunk)
                chunk_header = f"**🔗 Neural Chunk {i//20 + 1}:**\n{chunk_text}"
                await update.message.reply_text(chunk_header, parse_mode="Markdown")
                await asyncio.sleep(0.5)  # Prevent rate limiting

        # 💾 Deliver quantum files
        file_delivery_message = f"""
{CYBER_EMOJIS['data']} **QUANTUM FILES READY**
{create_cyber_divider()}
{CYBER_EMOJIS['matrix']} **JSON Log:** Advanced analytics data
{CYBER_EMOJIS['fire']} **TXT Results:** Clean formatted results
{CYBER_EMOJIS['hack']} **Developer:** {DEVELOPER_TAG}
        """
        
        try:
            # Send result.txt file (main user file)
            if result_filename and os.path.exists(result_filename):
                with open(result_filename, "rb") as f:
                    await update.message.reply_document(
                        document=f,
                        filename=f"nexus_results_{dork.replace(' ', '_')[:20]}.txt",
                        caption=f"{CYBER_EMOJIS['success']} **NEXUS QUANTUM RESULTS** | Query: `{dork}` | Results: {len(results)} | Dev: {DEVELOPER_TAG}"
                    )
                # Clean up temp file
                os.remove(result_filename)
            
            # Send JSON log file (advanced analytics)
            if os.path.exists("nexus_search_logs.json"):
                with open("nexus_search_logs.json", "rb") as f:
                    await update.message.reply_document(
                        document=f,
                        filename=f"nexus_analytics_{int(time.time())}.json",
                        caption=f"{CYBER_EMOJIS['neural']} **NEXUS ANALYTICS LOG** | Advanced Data | Dev: {DEVELOPER_TAG}"
                    )
                    
            await update.message.reply_text(file_delivery_message, parse_mode="Markdown")
            
        except Exception as e:
            logger.error(f"{CYBER_EMOJIS['error']} Quantum file delivery error: {e}")
            await update.message.reply_text(f"{CYBER_EMOJIS['warning']} **File delivery partially failed** | Contact: {DEVELOPER_TAG}")


    except Exception as e:
        logger.error(f"{CYBER_EMOJIS['error']} Quantum search disruption: {e}")
        error_message = f"""
{CYBER_EMOJIS['error']} **NEURAL SYSTEM ERROR**
{create_cyber_divider()}
{CYBER_EMOJIS['warning']} **Error:** `{str(e)}`
{CYBER_EMOJIS['gear']} **Contact:** {DEVELOPER_TAG}
        """
        await update.message.reply_text(error_message, parse_mode="Markdown")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🚀 Futuristic welcome experience"""
    if not update.message:
        return
    
    user_name = update.effective_user.first_name or "Neural User"
    welcome_message = f"""
{NEXUS_BANNER}

{CYBER_EMOJIS['star']} **Welcome to the Matrix, {user_name}!**

{CYBER_EMOJIS['neural']} **NEXUS CAPABILITIES:**
{create_cyber_divider()}
{CYBER_EMOJIS['search']} **Quantum Search** - Multi-source intelligence
{CYBER_EMOJIS['lightning']} **Neural Speed** - Lightning-fast results  
{CYBER_EMOJIS['shield']} **Cyber Security** - Anonymous & secure
{CYBER_EMOJIS['data']} **Analytics** - Advanced result processing
{CYBER_EMOJIS['quantum']} **Quantum Boost** - Enhanced accuracy

{CYBER_EMOJIS['hack']} **Developed by:** {DEVELOPER_TAG}
{CYBER_EMOJIS['fire']} **Version:** NEXUS v2.0
{CYBER_EMOJIS['rocket']} **Status:** Fully Operational

{create_cyber_divider()}
{CYBER_EMOJIS['target']} **Start with:** `/search <query> <count>`
    """
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode="Markdown",
        reply_markup=create_futuristic_keyboard()
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🎮 Handle futuristic button interactions"""
    query = update.callback_query
    await query.answer()
    
    responses = {
        "quick_search": f"{CYBER_EMOJIS['lightning']} **Quick Search Mode Activated**\nUse: `/search <query> 10`",
        "advanced_search": f"{CYBER_EMOJIS['gear']} **Advanced Search Protocol**\nUse: `/search \"complex query\" 50`",
        "analytics": f"{CYBER_EMOJIS['data']} **Neural Analytics Online**\nAdvanced result processing enabled",
        "security": f"{CYBER_EMOJIS['shield']} **Quantum Security Status**\nAll searches are encrypted and anonymous",
        "neural_mode": f"{CYBER_EMOJIS['neural']} **Neural Mode Engaged**\nAI-enhanced search patterns activated",
        "quantum_boost": f"{CYBER_EMOJIS['quantum']} **Quantum Boost Active**\nMaximum search accuracy enabled"
    }
    
    response = responses.get(query.data, f"{CYBER_EMOJIS['error']} Unknown command")
    await query.edit_message_text(f"{response}\n\n{CYBER_EMOJIS['hack']} **Developer:** {DEVELOPER_TAG}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📚 Advanced help system"""
    help_text = f"""
{CYBER_EMOJIS['robot']} **NEXUS NEURAL COMMAND CENTER**
{create_cyber_divider()}

{CYBER_EMOJIS['lightning']} **Basic Commands:**
• `/start` - Initialize neural interface
• `/search <dork> <count>` - Quantum search
• `/help` - Display this neural guide

{CYBER_EMOJIS['neural']} **Advanced Examples:**
• `/search inurl:admin 25` - Find admin panels
• `/search "site:github.com python" 50` - GitHub search
• `/search filetype:pdf cybersecurity 30` - PDF files

{CYBER_EMOJIS['quantum']} **Quantum Features:**
• Multi-source aggregation
• Neural deduplication
• Quantum result optimization
• Encrypted data streams

{CYBER_EMOJIS['fire']} **Developer:** {DEVELOPER_TAG}
{CYBER_EMOJIS['star']} **Version:** NEXUS v2.0
{create_cyber_divider()}
{CYBER_EMOJIS['rocket']} **Ready for quantum operations!**
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def set_commands(application):
    """🎯 Set futuristic bot commands"""
    commands = [
        BotCommand("start", "🚀 Initialize NEXUS interface"),
        BotCommand("search", "🔍 Quantum search engine"),
        BotCommand("help", "📚 Neural command guide"),
    ]
    await application.bot.set_my_commands(commands)

def main():
    """🚀 Launch the NEXUS quantum system"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error(f"{CYBER_EMOJIS['error']} Neural link failed - TELEGRAM_BOT_TOKEN missing")
        return

    if not SERPAPI_KEY:
        logger.warning(f"{CYBER_EMOJIS['warning']} SerpAPI neural link offline - DuckDuckGo only")

    try:
        print(NEXUS_BANNER)
        logger.info(f"{CYBER_EMOJIS['rocket']} NEXUS neural networks initializing...")
        
        # 🌐 Initialize quantum application
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        # 🎯 Register neural handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("search", search_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CallbackQueryHandler(button_callback))

        # 🚀 Set quantum commands
        app.job_queue.run_once(lambda context: set_commands(app), when=1)

        logger.info(f"{CYBER_EMOJIS['success']} NEXUS quantum system online!")
        logger.info(f"{CYBER_EMOJIS['hack']} Developed by: {DEVELOPER_TAG}")
        
        # 🌟 Launch neural interface
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"{CYBER_EMOJIS['error']} Quantum system failure: {e}")

if __name__ == '__main__':
    main()
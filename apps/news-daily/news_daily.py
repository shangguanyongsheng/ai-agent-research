#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "rich", "python-dateutil", "beautifulsoup4"]
# ///
"""
AI 新闻日报生成器 v3.2
- 接入 xix.ai 高质量 AI 新闻源
- 结构化大模型评测数据
- 硅谷科技媒体动态
- X/Twitter AI 大牛动态（via Nitter）
- 优化 QQ 消息格式
"""

import os
import sys
import json
import re
import requests
from datetime import datetime, timedelta
from rich.console import Console
from dateutil import parser as date_parser
from bs4 import BeautifulSoup

console = Console()

# 配置
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")
XIX_AI_URL = "https://xix.ai/zh/live"

# 硅谷新闻源（需要代理）
SILICON_VALLEY_SOURCES = {
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/",
    "theverge_ai": "https://www.theverge.com/ai-artificial-intelligence",
    "venturebeat_ai": "https://venturebeat.com/category/ai/",
    "wired_ai": "https://www.wired.com/tag/artificial-intelligence/",
}

# 启用代理的 session（用于访问硅谷源）
proxy_session = requests.Session()
# 从环境变量读取代理配置
proxy_session.trust_env = True  # 使用系统代理环境变量

# 禁用代理的 session（用于国内源）
session = requests.Session()
session.trust_env = False


def fetch_xix_ai_news() -> list:
    """从 xix.ai 获取高质量 AI 新闻"""
    console.print("[yellow]📡 从 xix.ai 获取 AI 新闻...[/yellow]")
    
    try:
        response = session.get(
            XIX_AI_URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        response.raise_for_status()
        
        # 解析 HTML 提取 JSON-LD 数据
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找 JSON-LD 脚本
        news_items = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and 'itemListElement' in data:
                    for item in data['itemListElement']:
                        if item.get('item', {}).get('@type') == 'NewsArticle':
                            article = item['item']
                            news_items.append({
                                'title': article.get('headline', ''),
                                'description': article.get('description', ''),
                                'date': article.get('datePublished', ''),
                                'url': article.get('url', ''),
                            })
            except (json.JSONDecodeError, KeyError):
                continue
        
        console.print(f"[green]✓ 获取到 {len(news_items)} 条新闻[/green]")
        return news_items
        
    except Exception as e:
        console.print(f"[red]获取 xix.ai 失败: {e}[/red]")
        return []


def search_searxng(query: str, limit: int = 10, time_range: str = "week") -> list:
    """使用 SearXNG 搜索（备用）"""
    params = {
        "q": query,
        "format": "json",
        "categories": "general",
        "time_range": time_range,
        "language": "auto",
    }
    
    try:
        response = session.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])[:limit]
    except Exception as e:
        console.print(f"[red]搜索失败:[/red] {e}")
        return []


def fetch_silicon_valley_news() -> list:
    """从硅谷科技媒体获取 AI 新闻（需要代理）"""
    console.print("[yellow]🌐 从硅谷科技媒体获取 AI 新闻...[/yellow]")
    
    news_items = []
    
    # 方法1: 使用 SearXNG 搜索英文关键词
    queries = [
        "OpenAI GPT news site:techcrunch.com OR site:theverge.com OR site:venturebeat.com",
        "Anthropic Claude news site:techcrunch.com OR site:theverge.com",
        "AI startup funding Silicon Valley 2026",
        "Google DeepMind Gemini news latest",
        "Meta AI Llama news release",
    ]
    
    for query in queries:
        try:
            results = search_searxng(query, limit=5, time_range="week")
            for result in results:
                title = result.get('title', '')
                url = result.get('url', '')
                content = result.get('content', '')[:200]
                date = result.get('publishedDate', '')
                
                # 过滤掉中文结果
                if any(c in title + content for c in '的是在有了不这'):
                    continue
                
                news_items.append({
                    'title': title,
                    'description': content,
                    'date': date,
                    'url': url,
                    'source': 'silicon_valley'
                })
        except Exception as e:
            console.print(f"[red]搜索失败: {query[:30]}... - {e}[/red]")
    
    # 去重
    seen_urls = set()
    unique_items = []
    for item in news_items:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_items.append(item)
    
    console.print(f"[green]✓ 获取到 {len(unique_items)} 条硅谷新闻[/green]")
    return unique_items[:10]


# X/Twitter AI 大牛账号列表（通过 Nitter 抓取）
AI_TWITTER_ACCOUNTS = [
    {"handle": "karpathy", "name": "Andrej Karpathy", "desc": "OpenAI 前 researcher，AI 教育者"},
    {"handle": "sama", "name": "Sam Altman", "desc": "OpenAI CEO"},
    {"handle": "ylecun", "name": "Yann LeCun", "desc": "Meta AI 首席科学家，图灵奖得主"},
    {"handle": "AndrewYNg", "name": "Andrew Ng", "desc": "吴恩达，AI 教育先驱"},
    {"handle": "EMostaque", "name": "Emad Mostaque", "desc": "Stability AI 创始人"},
]

# Nitter 实例列表（公共镜像）
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.net",
    "https://nitter.unixfox.eu",
    "https://nitter.kavin.rocks",
]


def fetch_hackernews_ai() -> list:
    """从 Hacker News 获取 AI 相关热门内容"""
    console.print("[yellow]🔥 从 Hacker News 获取 AI 热门...[/yellow]")
    
    items = []
    
    try:
        # Hacker News Top Stories API
        response = proxy_session.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=15
        )
        story_ids = response.json()[:50]  # 取前 50 个
        
        # AI 相关关键词
        ai_keywords = [
            'ai', 'ml', 'gpt', 'llm', 'openai', 'anthropic', 'deepmind',
            'machine learning', 'neural', 'transformer', 'chatbot',
            'artificial intelligence', 'claude', 'gemini', 'llama'
        ]
        
        for story_id in story_ids[:30]:
            try:
                story_resp = proxy_session.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=10
                )
                story = story_resp.json()
                
                if not story:
                    continue
                
                title = story.get('title', '').lower()
                url = story.get('url', '')
                score = story.get('score', 0)
                
                # 检查是否 AI 相关
                if any(kw in title for kw in ai_keywords) and score >= 50:
                    items.append({
                        'title': story.get('title', ''),
                        'url': url or f"https://news.ycombinator.com/item?id={story_id}",
                        'score': score,
                        'comments': story.get('descendants', 0),
                        'source': 'hackernews'
                    })
                
                if len(items) >= 5:
                    break
                    
            except:
                continue
        
        console.print(f"[green]✓ 获取到 {len(items)} 条 HN AI 热门[/green]")
        
    except Exception as e:
        console.print(f"[red]Hacker News 获取失败: {e}[/red]")
    
    return items


def fetch_x_ai_tweets() -> list:
    """从 X/Twitter 抓取 AI 大牛动态（via Nitter）"""
    console.print("[yellow]🐦 从 X/Twitter 获取 AI 大牛动态...[/yellow]")
    
    tweets = []
    
    for account in AI_TWITTER_ACCOUNTS:
        success = False
        
        # 尝试多个 Nitter 实例
        for nitter_base in NITTER_INSTANCES:
            if success:
                break
                
            try:
                url = f"{nitter_base}/{account['handle']}"
                response = proxy_session.get(
                    url,
                    timeout=15,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )
                
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析推文
                tweet_items = soup.select('.timeline-item')[:3]  # 取最近 3 条
                
                for item in tweet_items:
                    tweet_text = item.select_one('.tweet-content')
                    tweet_link = item.select_one('a.tweet-link')
                    
                    if tweet_text and tweet_link:
                        text = tweet_text.get_text(strip=True)[:200]
                        link = f"https://twitter.com{tweet_link.get('href', '')}"
                        
                        # 过滤掉太短或无意义的内容
                        if len(text) > 20 and not text.startswith('RT @'):
                            tweets.append({
                                'author': account['name'],
                                'handle': account['handle'],
                                'desc': account['desc'],
                                'text': text,
                                'url': link,
                                'source': 'twitter'
                            })
                
                success = True
                console.print(f"[green]✓ {account['name']}: 获取成功 ({nitter_base})[/green]")
                
            except Exception as e:
                continue
        
        if not success:
            console.print(f"[yellow]⚠ {account['name']}: 所有实例均失败[/yellow]")
    
    console.print(f"[green]✓ 获取到 {len(tweets)} 条推文[/green]")
    return tweets


def fetch_model_benchmarks() -> list:
    """获取最新大模型评测数据"""
    console.print("[yellow]📊 获取大模型评测数据...[/yellow]")
    
    # 搜索评测相关
    queries = [
        "大模型评测 榜单 排名 2026",
        "LLM benchmark leaderboard latest",
        "GPT Claude Qwen DeepSeek 新模型 发布",
    ]
    
    all_results = []
    for query in queries:
        results = search_searxng(query, limit=10, time_range="week")
        all_results.extend(results)
    
    # 去重并筛选
    seen_urls = set()
    benchmarks = []
    
    # 模型关键词
    model_keywords = [
        "gpt", "claude", "qwen", "llama", "gemini", "deepseek",
        "mistral", "kimi", "chatglm", "yi", "baichuan", "zhipu",
        "moonshot", "doubao", "ernie", "通义", "文心", "智谱",
        "openai", "anthropic", "google", "meta", "alibaba"
    ]
    
    # 评测/发布关键词
    bench_keywords = [
        "评测", "排名", "benchmark", "leaderboard", "榜单",
        "发布", "推出", "超越", "登顶", "开源", "最新", "new release"
    ]
    
    for result in all_results:
        url = result.get("url", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        
        has_model = any(kw in title or kw in content for kw in model_keywords)
        has_bench = any(kw in title or kw in content for kw in bench_keywords)
        
        if has_model and has_bench:
            benchmarks.append({
                'title': result.get('title', ''),
                'description': result.get('content', '')[:150],
                'date': result.get('publishedDate', ''),
                'url': url,
            })
    
    return benchmarks[:6]


def format_date(date_str: str) -> str:
    """格式化日期"""
    if not date_str:
        return "未知"
    try:
        dt = date_parser.parse(date_str)
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours == 0:
                return "刚刚"
            return f"{hours}小时前"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            return dt.strftime("%m-%d")
    except:
        return "未知"


def parse_news_items(text: str) -> list:
    """从新闻文本中解析独立的新闻条目"""
    items = []
    
    # 按中文句号分割，每句话是一条新闻
    sentences = re.split(r'[。！？]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 15:
            continue
        
        # 截断过长的句子
        if len(sentence) > 60:
            # 尝试在逗号处截断
            parts = sentence.split('，')
            if len(parts) > 1:
                sentence = parts[0] + '，' + parts[1][:30] + '...'
            else:
                sentence = sentence[:60] + '...'
        
        items.append(sentence)
    
    return items[:4]  # 最多4条，保持简洁


def render_qq_message(report: dict) -> str:
    """渲染为 QQ 消息格式"""
    date = report["date"]
    time_str = report["time"]
    
    msg = f"""╔════════════════════════════════════════════╗
║          📰 AI 新闻日报 v3.2                ║
║          日期：{date}                        ║
╚════════════════════════════════════════════╝

"""
    
    # Hacker News AI 热门（新增）
    if report.get("hn_items"):
        msg += "🔥 Hacker News AI 热门\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, item in enumerate(report["hn_items"][:5], 1):
            title = item.get('title', '')[:45]
            if len(item.get('title', '')) > 45:
                title += "..."
            score = item.get('score', 0)
            comments = item.get('comments', 0)
            
            msg += f"【{i}】{title}\n"
            msg += f"    👍 {score} 💬 {comments}\n\n"
    
    # X/Twitter AI 大牛动态（如果有）
    if report.get("tweets"):
        msg += "\n🐦 X/Twitter AI 动态\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, tweet in enumerate(report["tweets"][:4], 1):
            author = tweet.get('author', '')
            handle = tweet.get('handle', '')
            text = tweet.get('text', '')[:70]
            if len(tweet.get('text', '')) > 70:
                text += "..."
            
            msg += f"【{i}】@{handle}\n"
            msg += f"    💬 {text}\n\n"
    
    # 硅谷 AI 新闻
    news_index = 0
    if report.get("silicon_news"):
        msg += "\n🌐 硅谷 AI 新闻\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for item in report["silicon_news"][:3]:
            news_index += 1
            title = item.get('title', '')[:40]
            if len(item.get('title', '')) > 40:
                title += "..."
            
            msg += f"【{news_index}】{title}\n\n"
            
            if news_index >= 3:
                break
    
    # 国内 AI 新闻
    if report.get("news"):
        msg += "\n🤖 国内 AI 新闻\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for item in report["news"][:2]:
            description = item.get('description', '')
            news_points = parse_news_items(description)
            
            for point in news_points:
                news_index += 1
                msg += f"【{news_index}】{point}\n\n"
                
                if news_index >= 8:
                    break
            
            if news_index >= 8:
                break
    
    msg += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 数据来源：Hacker News + 硅谷媒体 + xix.ai
⏰ 推送时间：每天早上 8:50
"""
    
    return msg


def render_markdown_report(report: dict) -> str:
    """渲染为 Markdown 格式"""
    date = report["date"]
    time_str = report["time"]
    
    md = f"""# 📰 AI 新闻日报

**日期**: {date}  
**生成时间**: {time_str}

---

## 🤖 AI 新闻精选

"""
    
    for i, item in enumerate(report["news"][:5], 1):
        title = item.get('title', '无标题')
        date_str = format_date(item.get('date', ''))
        description = item.get('description', '')
        url = item.get('url', '')
        
        md += f"""### {i}. {title}

- **时间**: {date_str}
- **摘要**: {description}
- **来源**: [{url}]({url})

"""
    
    if report["benchmarks"]:
        md += """---

## 📊 大模型评测动态

| 序号 | 标题 | 时间 | 链接 |
|------|------|------|------|
"""
        for i, item in enumerate(report["benchmarks"], 1):
            title = item.get('title', '无标题')[:40]
            date_str = format_date(item.get('date', ''))
            url = item.get('url', '')
            md += f"| {i} | {title} | {date_str} | [链接]({url}) |\n"
    
    md += """

---

*📰 AI 新闻日报生成器 v3.0*  
*📡 数据来源：xix.ai + SearXNG*  
*⏰ 推送时间：每天早上 8:50*
"""
    
    return md


def generate_daily_report() -> dict:
    """生成日报数据"""
    date = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    
    console.print(f"\n[bold cyan]📰 生成 {date} AI 新闻日报 v3.2...[/bold cyan]\n")
    
    # 获取 xix.ai 新闻（国内）
    news = fetch_xix_ai_news()
    
    # 获取硅谷新闻（国外）
    silicon_news = fetch_silicon_valley_news()
    
    # 获取 Hacker News AI 热门
    hn_items = fetch_hackernews_ai()
    
    # 获取 X/Twitter AI 大牛动态（可能失败）
    tweets = fetch_x_ai_tweets()
    
    # 获取评测数据
    benchmarks = fetch_model_benchmarks()
    
    console.print(f"[green]✓ 国内 AI 新闻: {len(news)} 条[/green]")
    console.print(f"[green]✓ 硅谷 AI 新闻: {len(silicon_news)} 条[/green]")
    console.print(f"[green]✓ Hacker News 热门: {len(hn_items)} 条[/green]")
    console.print(f"[green]✓ X/Twitter 动态: {len(tweets)} 条[/green]")
    console.print(f"[green]✓ 评测动态: {len(benchmarks)} 条[/green]\n")
    
    return {
        "date": date,
        "time": time_str,
        "news": news,
        "silicon_news": silicon_news,
        "hn_items": hn_items,
        "tweets": tweets,
        "benchmarks": benchmarks
    }


def save_report(report: dict, output_dir: str = "./reports"):
    """保存报告到文件"""
    os.makedirs(output_dir, exist_ok=True)
    date = report["date"].replace("-", "")
    
    # 保存 Markdown 版本
    md_path = f"{output_dir}/ai_news_{date}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown_report(report))
    console.print(f"[green]✓ 报告已保存：{md_path}[/green]")
    
    # 保存 JSON 版本
    json_path = f"{output_dir}/ai_news_{date}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    console.print(f"[green]✓ 数据已保存：{json_path}[/green]")
    
    return md_path, json_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI 新闻日报生成器 v3.0")
    parser.add_argument("--date", "-d", help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--output", "-o", default="./reports", help="输出目录")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "qq", "all"], 
                       default="all", help="输出格式")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")
    args = parser.parse_args()
    
    if args.quiet:
        global console
        console = Console(file=open(os.devnull, "w"))
    
    # 生成日报
    report = generate_daily_report()
    
    # 输出
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.format == "qq":
        print(render_qq_message(report))
    elif args.format == "markdown":
        print(render_markdown_report(report))
    else:
        md_path, json_path = save_report(report, args.output)
        console.print(f"\n[bold green]✓ 日报生成完成![/bold green]")
        console.print(f"📄 Markdown: {md_path}")
        console.print(f"📊 JSON: {json_path}")


if __name__ == "__main__":
    main()
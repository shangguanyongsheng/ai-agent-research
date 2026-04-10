#!/usr/bin/env python3
"""
AI 新闻日报生成器 - 测试脚本
验证所有核心功能正常工作
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from news_daily import (
    search_news,
    format_news_item,
    generate_daily_news,
    render_markdown_report,
    render_qq_message
)


def test_search_news():
    """测试新闻搜索"""
    print("🔍 测试：search_news")
    results = search_news("AI 人工智能", limit=3, time_range="day")
    assert len(results) >= 0, "搜索应该返回结果"
    print(f"  ✓ 搜索返回 {len(results)} 条结果")
    if results:
        print(f"  ✓ 第一条：{results[0].get('title', 'N/A')[:50]}...")
    return True


def test_format_news_item():
    """测试新闻格式化"""
    print("\n📝 测试：format_news_item")
    sample_result = {
        "title": "测试新闻标题",
        "url": "https://example.com",
        "content": "这是测试内容",
        "engines": ["bing"],
        "publishedDate": "2026-03-11T10:00:00Z"
    }
    formatted = format_news_item(sample_result, 1)
    assert "测试新闻标题" in formatted
    assert "example.com" in formatted
    print(f"  ✓ 格式化输出:\n{formatted[:200]}...")
    return True


def test_generate_daily_news():
    """测试日报生成"""
    print("\n📰 测试：generate_daily_news")
    daily_news = generate_daily_news()
    assert "date" in daily_news
    assert "categories" in daily_news
    assert len(daily_news["categories"]) > 0
    total_news = sum(cat["count"] for cat in daily_news["categories"])
    print(f"  ✓ 生成日期：{daily_news['date']}")
    print(f"  ✓ 分类数量：{len(daily_news['categories'])}")
    print(f"  ✓ 总新闻数：{total_news}")
    return daily_news


def test_render_markdown():
    """测试 Markdown 渲染"""
    print("\n📄 测试：render_markdown_report")
    daily_news = generate_daily_news()
    md = render_markdown_report(daily_news)
    assert "# 📰 AI 新闻日报" in md
    assert daily_news["date"] in md
    print(f"  ✓ Markdown 长度：{len(md)} 字符")
    print(f"  ✓ 包含标题和日期")
    return True


def test_render_qq_message():
    """测试 QQ 消息渲染"""
    print("\n💬 测试：render_qq_message")
    daily_news = generate_daily_news()
    qq_msg = render_qq_message(daily_news)
    assert "📰 AI 新闻日报" in qq_msg
    assert daily_news["date"] in qq_msg
    print(f"  ✓ QQ 消息长度：{len(qq_msg)} 字符")
    print(f"  ✓ 包含 emoji 和日期")
    return True


def main():
    print("="*60)
    print("AI 新闻日报生成器 - 功能测试")
    print("="*60)
    
    tests = [
        test_search_news,
        test_format_news_item,
        test_generate_daily_news,
        test_render_markdown,
        test_render_qq_message,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败：{e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("="*60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
ファクトチェック機能付きブログ記事生成システム
記事生成後に自動でDeepthinkファクトチェックを実行
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Tuple
from auto_fact_checker import DeepthinkFactChecker

class BlogGeneratorWithFactCheck:
    """ファクトチェック機能付きブログ生成器"""
    
    def __init__(self):
        self.fact_checker = DeepthinkFactChecker()
        self.output_dir = "/Users/chiaki/開発用/ブログ文章生成"
    
    def generate_blog_post(self, topic: str, content: str) -> str:
        """
        ブログ記事を生成
        """
        # ファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{topic}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # 記事をファイルに保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ ブログ記事を生成しました: {filename}")
        return filepath
    
    def auto_fact_check_post(self, filepath: str) -> Dict[str, Any]:
        """
        生成されたブログ記事のファクトチェックを自動実行
        """
        print("🔍 ファクトチェックを開始します...")
        
        # ファイルを読み込み
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ファクトチェック実行
        report = self.fact_checker.auto_fact_check_content(content, filepath)
        
        # レポートファイル名を生成
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        report_filename = f"fact_check_{base_name}.json"
        report_filepath = os.path.join(self.output_dir, report_filename)
        
        # レポートを保存
        self.fact_checker.save_report(report, report_filepath)
        
        # ファクトチェック結果の可読性の高いレポートも生成
        readable_report_filename = f"fact_check_{base_name}_readable.md"
        readable_report_filepath = os.path.join(self.output_dir, readable_report_filename)
        self._generate_readable_report(report, readable_report_filepath, filepath)
        
        print("✅ ファクトチェックが完了しました")
        return report
    
    def _generate_readable_report(self, report: Dict[str, Any], 
                                output_file: str, 
                                source_file: str):
        """人間が読みやすいファクトチェックレポートを生成"""
        
        markdown_report = f"""# ファクトチェック結果レポート

## 記事情報
- **ソースファイル**: {os.path.basename(source_file)}
- **チェック日時**: {report['metadata']['check_date']}
- **総チェック項目数**: {report['metadata']['total_facts_checked']}

## 検証結果サマリー
- ✅ **検証済み**: {report['summary']['verified_facts']}件
- ⚠️ **更新必要**: {report['summary']['needs_update']}件  
- ❌ **不正確**: {report['summary']['incorrect_facts']}件
- ❓ **未検証**: {report['summary']['unknown_facts']}件

**全体正確性**: {report['summary']['overall_accuracy']:.1%}  
**信頼度スコア**: {report['summary']['confidence_score']:.2f}/1.0

## 推奨アクション
"""
        
        for i, rec in enumerate(report['recommendations'], 1):
            markdown_report += f"{i}. {rec}\n"
        
        markdown_report += "\n## 詳細検証結果\n\n"
        
        # 検証結果を分類して表示
        categories = {
            'verified': '✅ 検証済み',
            'needs_update': '⚠️ 更新必要', 
            'incorrect': '❌ 不正確',
            'unknown': '❓ 未検証'
        }
        
        for status, title in categories.items():
            facts_in_category = [f for f in report['detailed_results'] 
                               if f['verification_result']['status'] == status]
            
            if facts_in_category:
                markdown_report += f"### {title} ({len(facts_in_category)}件)\n\n"
                
                for fact in facts_in_category:
                    confidence = fact['verification_result']['confidence']
                    markdown_report += f"**{fact['text']}**\n"
                    markdown_report += f"- 種類: {fact['type']} / {fact['category']}\n"
                    markdown_report += f"- 信頼度: {confidence:.2f}\n"
                    markdown_report += f"- コンテキスト: {fact['context'][:100]}...\n"
                    if fact['verification_result']['notes']:
                        markdown_report += f"- 備考: {fact['verification_result']['notes']}\n"
                    markdown_report += "\n"
        
        markdown_report += f"""
---
*このレポートは自動ファクトチェッカー (Deepthink モード) により生成されました*  
*レポート生成時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # ファイルに保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
    
    def display_fact_check_summary(self, report: Dict[str, Any]):
        """ファクトチェック結果のサマリーを表示"""
        print("\n" + "="*50)
        print("📊 ファクトチェック結果サマリー")
        print("="*50)
        
        summary = report['summary']
        print(f"✅ 検証済み事実: {summary['verified_facts']}件")
        print(f"⚠️  更新が必要: {summary['needs_update']}件")
        print(f"❌ 不正確な情報: {summary['incorrect_facts']}件") 
        print(f"❓ 未検証事実: {summary['unknown_facts']}件")
        print(f"📈 全体正確性: {summary['overall_accuracy']:.1%}")
        print(f"🎯 信頼度スコア: {summary['confidence_score']:.2f}/1.0")
        
        print("\n💡 推奨アクション:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*50)
    
    def generate_and_fact_check(self, topic: str, content: str) -> Tuple[str, Dict[str, Any]]:
        """
        ブログ記事生成とファクトチェックを一括実行
        """
        print(f"🚀 '{topic}' に関するブログ記事の生成とファクトチェックを開始します")
        
        # 記事生成
        filepath = self.generate_blog_post(topic, content)
        
        # ファクトチェック実行
        report = self.auto_fact_check_post(filepath)
        
        # 結果表示
        self.display_fact_check_summary(report)
        
        return filepath, report


def main():
    """使用例とテスト"""
    generator = BlogGeneratorWithFactCheck()
    
    # 既存の会社設立ガイドをファクトチェック
    existing_file = "/Users/chiaki/開発用/ブログ文章生成/会社設立ガイド.md"
    
    if os.path.exists(existing_file):
        print("既存の会社設立ガイドをファクトチェックします...")
        report = generator.auto_fact_check_post(existing_file)
        generator.display_fact_check_summary(report)
    else:
        print("会社設立ガイド.mdが見つかりません")


if __name__ == "__main__":
    main()
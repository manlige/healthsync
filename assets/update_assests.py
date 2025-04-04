# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 15:20:56 2025

@author: mandy_dmhrm46
"""

import os
import shutil
from bs4 import BeautifulSoup
import re

def update_assets():
    # 设置路径
    base_path = r"C:\MG\UCC Study\12_IS6153_Application Design\02_Assignment_IS6153\01_Assignment_Group\High-fi"
    assets_path = os.path.join(base_path, 'assets')
    
    # 备份现有的assets文件夹
    if os.path.exists(assets_path):
        backup_path = assets_path + '_backup'
        try:
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            shutil.move(assets_path, backup_path)
            print(f"已备份现有assets文件夹到: {backup_path}")
        except Exception as e:
            print(f"备份assets文件夹时出错: {str(e)}")

    # 创建新的assets文件夹结构
    try:
        os.makedirs(os.path.join(assets_path, 'icons'))
        os.makedirs(os.path.join(assets_path, 'css'))
        os.makedirs(os.path.join(assets_path, 'js'))
        print("已创建新的assets文件夹结构")
    except Exception as e:
        print(f"创建文件夹结构时出错: {str(e)}")

    # 创建常用图标的SVG文件
    icons = {
        'home': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 3L4 9v12h16V9l-8-6z"/>
        </svg>''',
        'calendar': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
        </svg>''',
        'health': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>''',
        'insights': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
        </svg>''',
        'profile': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>'''
    }

    # 保存图标文件
    for icon_name, svg_content in icons.items():
        try:
            with open(os.path.join(assets_path, 'icons', f'{icon_name}.svg'), 'w', encoding='utf-8') as f:
                f.write(svg_content)
        except Exception as e:
            print(f"保存{icon_name}图标时出错: {str(e)}")

    # 创建基础CSS文件
    base_css = '''
/* 基础样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

body {
    background: #f5f9fb;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* 导航栏样式 */
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: space-around;
    background: white;
    padding: 1rem 0;
    border-top: 1px solid #eee;
}

.nav-item {
    text-align: center;
    color: #808080;
    cursor: pointer;
    transition: color 0.3s ease;
}

.nav-item.active {
    color: #2A9D8F;
}

/* 响应式设计 */
@media (max-width: 768px) {
    body {
        padding: 1rem;
    }
}
'''

    try:
        with open(os.path.join(assets_path, 'css', 'style.css'), 'w', encoding='utf-8') as f:
            f.write(base_css)
        print("已创建基础CSS文件")
    except Exception as e:
        print(f"创建CSS文件时出错: {str(e)}")

    # 分析所有HTML文件
    html_files = [f for f in os.listdir(base_path) if f.endswith('.html')]
    for html_file in html_files:
        try:
            with open(os.path.join(base_path, html_file), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            # 分析并提取内联样式和脚本
            styles = soup.find_all('style')
            scripts = soup.find_all('script')
            
            # 这里可以添加更多的分析和处理逻辑
            
        except Exception as e:
            print(f"分析{html_file}时出错: {str(e)}")

    print("\n资源文件更新完成！")
    print("1. 原有assets文件夹已备份")
    print("2. 新的assets文件夹已创建")
    print("3. 基础图标已生成")
    print("4. 基础CSS样式已创建")

if __name__ == "__main__":
    update_assets()
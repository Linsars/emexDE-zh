#!/usr/bin/env python3
"""
Generate zh-Hans.lproj/Localizable.strings and wrap source strings with NSLocalizedString.
"""
import os, re, json

WORK_DIR = '/var/minis/workspace/emexDE-zh'

# Chinese translations for all UI strings
TRANSLATIONS = {
    "Applications": "应用程序",
    "Projects": "项目",
    "Settings": "设置",
    "Toolchain": "工具链",
    "Certificate": "证书",
    "Customization": "个性化",
    "Kernel Log": "内核日志",
    "Credits": "致谢",
    "Project": "项目",
    "Application project": "应用项目",
    "Command line tool project": "命令行工具项目",
    "Library project": "库项目",
    "Product Name": "产品名称",
    "Organization Identifier": "组织标识符",
    "Bundle Identifier": "包标识符",
    "Display Name": "显示名称",
    "Bundle Version": "包版本",
    "Bundle Short Version": "短版本号",
    "Deployment Target": "部署目标",
    "Executable": "可执行文件",
    "Language:": "语言：",
    "Interface:": "界面：",
    "Swift": "Swift",
    "Objective-C": "Objective-C",
    "C++": "C++",
    "C": "C",
    "SwiftUI": "SwiftUI",
    "UIKit": "UIKit",
    "Cancel": "取消",
    "Previous": "上一步",
    "Next": "下一步",
    "Create": "创建",
    "Done": "完成",
    "Close": "关闭",
    "Save": "保存",
    "Save File": "保存文件",
    "Open": "打开",
    "New": "新建",
    "Delete": "删除",
    "Rename": "重命名",
    "Copy": "复制",
    "Paste": "粘贴",
    "Move": "移动",
    "Share": "分享",
    "Export": "导出",
    "Import": "导入",
    "Import Certificate": "导入证书",
    "Install": "安装",
    "Run": "运行",
    "Build": "构建",
    "Refresh": "刷新",
    "Apply": "应用",
    "Configure": "配置",
    "Select": "选择",
    "Submit": "提交",
    "Continue": "继续",
    "OK": "确定",
    "Warning": "警告",
    "Name": "名称",
    "Filename": "文件名",
    "Folder": "文件夹",
    "File": "文件",
    "Utility": "工具",
    "App": "应用",
    "Development": "开发",
    "System": "系统",
    "Internal": "内部",
    "Theme": "主题",
    "Font Size": "字体大小",
    "Autoindent": "自动缩进",
    "Wrap Lines": "自动换行",
    "Show Line Numbers": "显示行号",
    "Show Line Breaks": "显示换行符",
    "Show Spaces": "显示空格",
    "Use Threads": "使用线程",
    "Contains no messages": "没有消息",
    "No Definition Found": "未找到定义",
    "Copied": "已复制",
    "Switcher": "切换器",
    "Host Manager": "主机管理",
    "Hostname": "主机名",
    "Username": "用户名",
    "Credentials Manager": "凭证管理",
    "Host & Credentials": "主机与凭证",
    "Set Service Endpoint": "设置服务端点",
    "Get Service Endpoint": "获取服务端点",
    "Start Service": "启动服务",
    "Stop Service": "停止服务",
    "Toggle Service": "切换服务",
    "Service": "服务",
    "Linker": "链接器",
    "Add Flag": "添加标志",
    "Edit Flag": "编辑标志",
    "Add Flag…": "添加标志…",
    "Incremental Build": "增量构建",
    "Clear Data Container": "清除数据容器",
    "Clear Module Cache": "清除模块缓存",
    "Clear Project Cache": "清除项目缓存",
    "Browse Cache": "浏览缓存",
    "Browse SDK": "浏览 SDK",
    "Project Configuration": "项目配置",
    "Additional Flags": "附加标志",
    "Security & Runtime": "安全与运行时",
    "Task & Process Access": "任务与进程访问",
    "Process Control": "进程控制",
    "Process Spawn": "进程派生",
    "Process Kill": "进程终止",
    "Process Enumeration": "进程枚举",
    "Process Elevate": "进程提权",
    "Process Spawn (Signed Only)": "进程派生（仅签名）",
    "Task for Pid": "Task for Pid",
    "Get Task Allowed": "允许获取 Task",
    "Patch Entitlements": "修补授权",
    "Platform Process": "平台进程",
    "Platform Root": "平台根目录",
    "Native Performance": "原生性能",
    "DYLD Hide LiveProcess": "隐藏 LiveProcess",
    "Inherit Entitlements on Spawn": "派生时继承授权",
    "Launch Services": "启动服务",
    "MobileDevelopmentKit": "MobileDevelopmentKit",
    "Issue Navigator": "问题导航",
    "Jump To Definition": "跳转到定义",
    "Validating": "验证中…",
    "Installing": "安装中…",
    "Editing": "编辑中…",
    "Hello, world!": "你好，世界！",
    "Hello": "你好",
    "1.0": "1.0",
    "This action cannot be undone.": "此操作无法撤销。",
    "Are you sure you want to remove": "确定要删除",
    "The log has been copied to the clipboard.": "日志已复制到剪贴板。",
    "A fatal error has happened finding code files.": "查找代码文件时发生致命错误。",
    "Nothing to build. No code files were found, please create a code file.": "没有可构建的内容。未找到代码文件，请创建一个代码文件。",
    "Could not find a definition for the symbol at the cursor.": "未能找到光标处符号的定义。",
    "NSExtension missing, make sure you keep the extension when installing.": "缺少 NSExtension，安装时请确保保留扩展。",
    "Kernel logging disabled.": "内核日志已禁用。",
    "Contributions, feedback, and stars keep the project alive.": "贡献、反馈和星标让项目保持活力。",
    "com.example": "com.example",
    "com.nyxian.example": "com.nyxian.example",
    "iOS": "iOS",
    "Output": "输出",
    "Input": "输入",
    "Module Cache": "模块缓存",
    "Project Cache": "项目缓存",
    "Data Container": "数据容器",
    "Info": "信息",
    "Debug": "调试",
    "Release": "发布",
    "All": "全部",
    "None": "无",
    "Default": "默认",
    "Custom": "自定义",
    "Search": "搜索",
    "Filter": "筛选",
    "Sort": "排序",
    " ascending": "升序",
    " descending": "降序",
    "Yes": "是",
    "No": "否",
    "On": "开",
    "Off": "关",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "Unknown": "未知",
    "Error": "错误",
    "Success": "成功",
    "Failed": "失败",
    "Ready": "就绪",
    "Loading": "加载中…",
    "Waiting": "等待中…",
    "Completed": "已完成",
    "Start": "开始",
    "Stop": "停止",
    "Restart": "重启",
    "Reset": "重置",
    "Back": "返回",
    "Forward": "前进",
    "Home": "首页",
    "Menu": "菜单",
    "Help": "帮助",
    "About": "关于",
    "License": "许可",
    "Version": "版本",
    "Update": "更新",
    "Upgrade": "升级",
    "Download": "下载",
    "Upload": "上传",
    "Connect": "连接",
    "Disconnect": "断开",
    "Retry": "重试",
    "Try Again": "重试",
    "Ignore": "忽略",
    "Skip": "跳过",
    "Finish": "完成",
    "Quit": "退出",
    "Exit": "退出",
    "Terminate": "终止",
    "Activate": "激活",
    "Deactivate": "停用",
    "Register": "注册",
    "Unregister": "注销",
    "Subscribe": "订阅",
    "Unsubscribe": "取消订阅",
    "Accept": "接受",
    "Reject": "拒绝",
    "Allow": "允许",
    "Deny": "拒绝",
    "Grant": "授予",
    "Revoke": "撤销",
    "Confirm": "确认",
    "Decline": "拒绝",
    "Learn More": "了解更多",
    "Show More": "显示更多",
    "Show Less": "显示更少",
    "Expand": "展开",
    "Collapse": "收起",
    "Minimize": "最小化",
    "Maximize": "最大化",
    "Restore": "恢复",
    "Pin": "固定",
    "Unpin": "取消固定",
    "Lock": "锁定",
    "Unlock": "解锁",
    "Hide": "隐藏",
    "Show": "显示",
    "Reveal": "显示",
    "Clear": "清除",
    "Clean": "清理",
    "Remove": "移除",
    "Add": "添加",
    "Insert": "插入",
    "Replace": "替换",
    "Modify": "修改",
    "Edit": "编辑",
    "Generate": "生成",
    "Create New": "新建",
    "Properties": "属性",
    "Attributes": "属性",
    "Parameters": "参数",
    "Arguments": "参数",
    "Options": "选项",
    "Configuration": "配置",
    "Preferences": "偏好设置",
    "General": "通用",
    "Advanced": "高级",
    "Experimental": "实验性",
    "Deprecated": "已弃用",
    "Details": "详情",
    "Summary": "摘要",
    "Description": "描述",
    "More Info": "更多信息",
    "Activity": "活动",
    "Status": "状态",
    "Progress": "进度",
    "Result": "结果",
    "Output:": "输出：",
    "Errors": "错误",
    "Warnings": "警告",
    "Issues": "问题",
    "Messages": "消息",
    "Notifications": "通知",
    "Logs": "日志",
    "History": "历史",
    "Recent": "最近",
    "Favorites": "收藏",
    "Bookmarks": "书签",
    "Downloads": "下载",
    "Documents": "文档",
    "Projects Directory": "项目目录",
    "Desktop": "桌面",
    "Trash": "废纸篓",
    "Application": "应用程序",
    "Framework": "框架",
    "Library": "库",
    "Plugin": "插件",
    "Extension": "扩展",
    "Bundle": "捆绑包",
    "Package": "包",
    "Archive": "归档",
    "Compress": "压缩",
    "Extract": "解压",
    "Unzip": "解压",
    "Zip": "压缩",
    "Encrypt": "加密",
    "Decrypt": "解密",
    "Authenticate": "认证",
    "Authorize": "授权",
    "Verify": "验证",
    "Validate": "验证",
    "Check": "检查",
    "Review": "审查",
    "Approve": "批准",
    "Reject Changes": "拒绝更改",
    "Commit": "提交",
    "Push": "推送",
    "Pull": "拉取",
    "Fetch": "获取",
    "Merge": "合并",
    "Rebase": "变基",
    "Resolve": "解决",
    "Sync": "同步",
    "Publish": "发布",
    "Deploy": "部署",
    "Rollback": "回滚",
    "Backup": "备份",
    "Restore Backup": "恢复备份",
}

def translate_key(key):
    """Get translation for a key. Returns None if no translation available."""
    if key in TRANSLATIONS:
        return TRANSLATIONS[key]
    return None

def escape_strings_file_value(s):
    """Escape a string for .strings file format."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def find_relevant_files():
    """Find Swift/ObjC files that contain UI strings."""
    files = []
    for root, dirs, fnames in os.walk(WORK_DIR):
        for f in fnames:
            if not f.endswith(('.swift', '.m', '.mm')):
                continue
            path = os.path.join(root, f)
            if '/.' in path or path.startswith(WORK_DIR + '/.'):
                continue
            files.append(path)
    return files

def main():
    # Step 1: Create the Localizable.strings file
    localization_dir = os.path.join(WORK_DIR, 'Nyxian', 'zh-Hans.lproj')
    os.makedirs(localization_dir, exist_ok=True)
    
    strings_path = os.path.join(localization_dir, 'Localizable.strings')
    with open(strings_path, 'w', encoding='utf-8') as f:
        f.write('/* English - Chinese Simplified Localization */\n')
        f.write('/* Auto-generated by emexDE-zh localization script */\n\n')
        for key in sorted(TRANSLATIONS.keys()):
            val = TRANSLATIONS[key]
            f.write(f'"{key}" = "{escape_strings_file_value(val)}";\n')
    
    print(f"Created {strings_path} with {len(TRANSLATIONS)} entries")
    
    # Step 2: Modify source files to use NSLocalizedString
    # We'll focus on key patterns in UI files
    files = find_relevant_files()
    print(f"Found {len(files)} source files to check")
    
    # Track what we changed
    changes = []
    
    for filepath in files:
        relpath = os.path.relpath(filepath, WORK_DIR)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # Pattern: self.title = "SomeString" → self.title = NSLocalizedString("SomeString", comment: "")
        # Only for UI-relevant files
        for m in re.finditer(r'\.title\s*=\s*"([^"]{2,60})"', content):
            key = m.group(1)
            if key in TRANSLATIONS:
                old = m.group(0)
                new = f'.title = NSLocalizedString("{key}", comment: "")'
                content = content.replace(old, new, 1)
        
        # Pattern: textLabel?.text = "SomeString"
        for m in re.finditer(r'(textLabel\?\.text|text)\s*=\s*"([^"]{2,60})"', content):
            key = m.group(2)
            if key in TRANSLATIONS:
                prefix = m.group(1)
                old = m.group(0)
                new = f'{prefix} = NSLocalizedString("{key}", comment: "")'
                content = content.replace(old, new, 1)
        
        # Pattern: Button("SomeString") 
        for m in re.finditer(r'Button\(\s*"([^"]{2,60})"\s*[,\)]', content):
            key = m.group(1)
            if key in TRANSLATIONS:
                old = m.group(0)
                new = f'Button(NSLocalizedString("{key}", comment: ""){m.group(0)[len(m.group(1))+9:]}' if m.group(0).endswith(',') else f'Button(NSLocalizedString("{key}", comment: ""))'
                # More careful replacement
                full_match = m.group(0)
                trailing = full_match[len('Button("') + len(key):]  # should be ", ... ) or " )
                new = f'Button(NSLocalizedString("{key}", comment: ""){trailing}'
                content = content.replace(full_match, new, 1)
        
        # Pattern: title: "SomeString" (in alert or sheet context)
        for m in re.finditer(r'(title|message)\s*:\s*"([^"]{2,80})"', content):
            key = m.group(2)
            if key in TRANSLATIONS:
                prefix = m.group(1)
                old = m.group(0)
                # Be careful with Swift vs ObjC syntax
                new = f'{prefix}: NSLocalizedString("{key}", comment: "")'
                content = content.replace(old, new, 1)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            changes.append(relpath)
    
    print(f"\nModified {len(changes)} files:")
    for f in changes:
        print(f"  {f}")
    
    # Step 3: Also create InfoPlist.strings for Info.plist strings if needed
    # (CFBundleDisplayName etc. - but those aren't localized here typically)

if __name__ == '__main__':
    main()

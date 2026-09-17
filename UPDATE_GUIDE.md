# 个人主页维护说明

网站使用 sbryngelson/academic-website-template（Jekyll）。网站仓库在 `www/`，直接更新这里的 Markdown、YAML 和 BibTeX 文件。不要直接修改生成的 `_site/index.html`。

## 常用内容在哪改

| 内容 | 文件 |
| --- | --- |
| 姓名、职称、学校、邮箱、头像、Scholar/CV 链接、导航和主题色 | `_config.yml` |
| 首页个人简介和研究方向 | `_pages/home.md` |
| 论文（Publications 页） | `assets/ref.bib` |
| 新闻（最新在前，侧栏显示前 3 条） | `_data/news.yml` |
| 教学 | `_data/teaching.yml` |
| 奖项与资助存档（当前不展示） | `_data/awards.yml`、`_data/grants.yml` |
| 学术服务 | `_pages/services.md` |
| CV | 替换 `cv_wentao.pdf` |
| 论文 PDF / 图片 | `pub/` / `images/projects/` |
| 局部样式 | `_sass/components/_wentao.scss` |

YAML 使用空格缩进，不要用 Tab。新闻、教学、奖项和项目按文件中的顺序显示。Markdown 中 `**文字**` 表示加粗，`[文字](网址)` 表示链接。

## 新增新闻

把新条目加在 `_data/news.yml` 的列表顶部（若有 `---`，加在它下面）：

```yaml
- date: "09/2026"
  headline: "Our paper was accepted to ..."
```

新闻中可用 HTML 链接，例如 `headline: 'Invited talk at <a href="https://example.org">Example University</a>'`。

## 新增论文

把图片和 PDF 分别放进 `images/projects/` 和 `pub/`。在 `assets/ref.bib` 中新增一个条目：

```bibtex
@article{example2027,
  title = {Example Paper Title},
  author = {Xie, Wentao and Doe, Jane},
  journal = {Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies},
  year = {2027},
  image = {images/projects/example.jpg},
  file = {example.pdf},
  doi = {10.xxxx/example},
  video = {https://example.org/demo}
}
```

- `example2027` 是唯一标识，不能与其他论文重复。
- 所有论文仅在 Publications 页显示；Home 不展示论文，已有的 `selected` 字段可以忽略。
- `file` 只填 `pub/` 中的文件名；`image` 填从仓库根目录开始的相对路径。
- `doi` 只填 DOI 标识，不要填 `https://doi.org/` 前缀。
- 可选的 `code`、`video`、`talk`、`slides`、`url` 用完整网址；没有的字段删掉，不要留示例值。
- 会议论文使用 `@inproceedings` 和 `booktitle`，期刊论文使用 `@article` 和 `journal`。
- 论文按年份和月份降序排列。需要同年排序时可填写 `month = {7}` 等字段。
- 迁移的旧论文保留了 `display_authors`（如 `<b>Wentao Xie</b>`、`<u>学生名字</u>`、共同一作 `*`）和 `display_venue`，用来保持原来的展示形式。新论文可以不填，模板会按标准引用格式显示；若要同样的展示效果，两项一起填写。
- `award` 可选，用于论文获奖说明。自定义展示字段不会出现在可复制的 BibTeX 中。
- 现有 BibTeX 是根据旧主页迁移的简要信息；精确引用时可以用出版社导出的完整 BibTeX 替换标准字段，并保留图片、链接等自定义字段。

## 本地预览

在终端执行：

```bash
cd /Users/wentao/Projects/homepage/www
./scripts/site.sh serve
```

打开 <http://127.0.0.1:4000>。编辑内容后自动重新构建，刷新浏览器即可。修改 `_config.yml` 后需要 Ctrl+C 停止服务，再重新运行。结束预览同样按 Ctrl+C。

只编译、不启动服务：

```bash
./scripts/site.sh build
python3 scripts/check_links.py
```

生成结果在 `_site/`，它不需要提交到 Git。端口占用时用 `PORT=4001 ./scripts/site.sh serve`。

首次在新电脑使用：安装 Ruby 3.2 或以上和 Bundler，然后运行 `./scripts/site.sh setup`。当前电脑的脚本也可使用 Homebrew 自带的新版 Ruby，避开 macOS 系统的 Ruby 2.6；正式部署使用 GitHub Actions 中的 Ruby 4.0。

## 发布到 GitHub Pages

仓库的 Pages 发布方式为 **GitHub Actions**。更新内容后，在本地构建、检查并推送：

```bash
cd /Users/wentao/Projects/homepage/www
./scripts/site.sh build
git status
git add -A
git commit -m "Update academic website"
git push origin main
```

在仓库 **Actions → Build and Deploy** 中查看构建和部署状态。成功后访问 <https://xie-wentao.github.io/>。

之后每次更新内容，只需预览、提交并推送到 `main`，工作流会自动编译和发布。无需上传 `_site/`，也无需重新建仓库或更改网站地址。不要再使用旧的“Deploy from a branch”直接发布 Jekyll 源文件。

## 模板来源

旧版 jemdoc 页面与源码已删除。研究简介在 Home 维护；`pub/`、`images/` 和 CV 链接保持可访问。

模板来源与版本记录见 `TEMPLATE.md`，MIT 授权见 `LICENSE`。网站保留了模板的字体、配色、深色模式、导航、搜索和卡片样式，并适配现有论文图片与作者标注。

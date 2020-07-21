# text_label(Easy Mark)

![](https://img.shields.io/badge/Status-Developing-brightgreen.svg)

> A Vue.js project (front-end interface) for marking entities in texts(especially pdf paper).

> **Database** structure will be shared **soon**.

> Front-end and Back-end are both independent.

## Functions or Features
- Parse PDF paper into texts
- Add new entity class
- Mark entities in texts
- Support multi-user collaboration

## Preview
- Project Management
![](easy_mark1.png)

- Class Management
![](easy_mark2.png)

- Work Table
![](easy_mark3.png)


## Build Setup For Front-end

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Build Setup For Back-end

Add Vue Project Host in [origins](textlabel_backend/apiCore.py) For Security
Configure Database in [config](textlabel_backend/db_toolkit.py)

```bash
# install dependencies
pip install python-multipart
pip install uvicorn
pip install fastapi

# open services
uvicorn apiCore:app --reload --port 8000 --host 0.0.0.0
```

## Developer log
```bash
npm install -g vue-cli

vue init webpack text_label

npm install axios -S
npm i element-ui -S
# npm install goeasy -S not used
```

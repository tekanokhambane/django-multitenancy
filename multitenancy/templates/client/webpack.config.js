const MiniCssExtractPlugin = require("mini-css-extract-plugin");
//const postcssPresetEnv = require('postcss-preset-env');
const postcss = require('postcss');
const path = require('path');

module.exports = {
    entry: path.resolve(__dirname, 'src'),
    resolve: {
        extensions: ['', '.js', '.jsx', '.ts', '.tsx'],
        modules: [
            path.join(__dirname, 'node_modules')
        ]
    },
    resolveLoader: {
        modules: [
            path.join(__dirname, 'node_modules')
        ]
    },
    
    output:{
        path: path.join(__dirname, "./static/publicUser"),
        filename: "index.bundle.js",
        clean:true,
    },
    devServer:{
        historyApiFallback: true,
        watchFiles:["src/**/*"],
        port: 3000,
        open:true,
        hot:true,
        //static:true,
    },
    module:{
        rules:[
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use:{
                    loader:"babel-loader"
                }
            },
            {
                test: /\.svg$/,
                use: ['@svgr/webpack'],
              },
            {
                test: /\.css$/,
                use:[
                    //MiniCssExtractPlugin.loader,
                    "style-loader",
                    "css-loader",
                    "sass-loader",
                    "postcss-loader",
                    // {
                    //     loader: "postcss-loader",
                    //     options: {
                    //       postcssOptions: {
                    //         plugins: [
                    //           [
                    //             postcssPresetEnv(/* pluginOptions */)
                    //           ],
                    //         ],
                    //       },
                    //     },
                    // }
                ]
            },
            {
                test: /\.scss$/,
                use:[
                    //MiniCssExtractPlugin.loader,
                    "style-loader",
                    "css-loader",
                    "sass-loader",
                    "postcss-loader",
                    // {
                    //     loader: "postcss-loader",
                    //     options: {
                    //       postcssOptions: {
                    //         plugins: [
                    //           [
                    //             postcssPresetEnv(/* pluginOptions */)
                    //           ],
                    //         ],
                    //       },
                    //     },
                    // }
                ]
            },
            //  {
            //     test: /\.html$/i,
            //     loader: "html-loader",
            //   },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader'
            },
            {
                test: /\.json$/,
                loader: "json-loader"
            },
            {
                test: /\.png$/, 
                exclude: /node_modules/,
                type: 'asset/resource'
            },
            {
                test: /\.jpg$/, 
                exclude: /node_modules/,
                type: 'asset/resource'
            },{
                test: /\.jpeg$/, 
                exclude: /node_modules/,
                type: 'asset/resource'
            },
            {
                test: /\.pdf$/,
                exclude: '/node_modeuls/',
                loader:'file-loader'
            }
        ]
    },
    // plugins:[
    //     new MiniCssExtractPlugin(),
    // ]
}
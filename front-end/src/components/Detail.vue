
<template>
    <div id="blur">
    <section class="w3l-whyblock py-3">
        <el-container class="pb-lg-5 pb-md-4 pb-2">
            <el-header id="site-header" style="font-weight: bold;">
            <nav class="navbar navbar-expand-lg navbar-light">
                <a class="navbar-brand" style="color:grey; font-size: 25px; margin-left:5%;">
                    <i class="el-icon-back" @click="backhome()"></i>
                    </a>   
                </nav>
            </el-header>
            <div class="row m-0">
                <div class="col-lg-6 ps-0" style="margin-left:6%; margin-top:2%;">
                    <el-row>
                        <el-col :span=12>
                            <h4 class="title-style mb-4" style="float:center;font-weight:bold;color:darkred;">{{this.title}}</h4>
                            <!-- <img src="../assets/images/c1.jpg" style="max-width: 60%;height: auto;"></el-col> -->
                            <p v-if="this.rating == null"> No rating yet </p>
                            <el-rate
                                v-else
                                v-model="this.rating"
                                disabled
                                show-score
                                text-color="#ff9900"
                                score-template="{value} points"
                                style="margin-top: 20%;"
                            >
                            </el-rate>
                            </el-col>

                        <el-col :span=12>
                            <h5 style="color:crimson; font-weight: bold;">Ingredients: </h5> <br/>
                            <li v-for="(item,index) in this.ingredients" style="text-align: left;"> 
                                <i class="el-icon-star-off"></i>  
                                {{item}}
                            </li>
                        </el-col>
                       
                    </el-row> <el-divider></el-divider>
                    <div class="two-grids mt-3">
                        <h5 style="color:crimson; font-weight: bold;">Cooking Methods</h5> <br/>
                        <div v-for="(item, index) in this.directions">
                            <div v-if="index==0" class="grids_info">
                                <i class="el-icon-star-off"></i>
                                    <p style="text-align:left;">{{ item }}</p>   
                            </div>
                            <div v-else class="grids_info mt-xl-5 mt-lg-4 mt-5">
                                <i class="el-icon-star-off"></i>
                                <p style="text-align:left;">{{ item }}</p>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="col-lg-5 ps-0 ps-lg-4 mt-lg-0" style="position: relative; margin-top:5%;">
                    <el-carousel indicator-position="outside">
                        <el-carousel-item  v-for="(item, index) in urls" :key="index">
                            <img v-bind:src="item.url" alt="" style="height:100%; width:auto; border-radius: 10px;">
                            <!-- <img src="../assets/images/ab.jpg" alt="" style="height:100%; width:auto; border-radius: 10px;"> -->
                        </el-carousel-item>
                    </el-carousel>
           </div>
        </div> 
        
    </el-container>
    </section>
    </div>
    </template>
    
    <script>// @ts-nocheck

        export default{
            name:'Detail',
            data(){
                return{
                    title: '',
                    ingredients: [],
                    directions: [],
                    value: 3.7,
                    urls: [
                        {url:require('../assets/images/ab.jpg')},
                        {url:require('../assets/images/about.jpg')},
                        {url:require('../assets/images/about1.jpg')},
                        {url:require('../assets/images/about2.jpg')},

                    ]
                }
            },
            methods: {
                backhome(){
                    this.$router.push({
                        name: 'Homepage',  
                    });
                    window.location.reload();
                },
                goBack(){
                    this.$router.push({
                        name: 'SearchResult',  
                        params: {
                            result: this.result
                        }
                    });

                },
                beforeRouteLeave(to,from,next){
                    to.meta.keepAlive = true
                    next(0)
                }
            },
            created(){
                this.title = this.$route.params.title;
                this.ingredients = this.$route.params.ingredients;
                this.directions = this.$route.params.directions;
                this.rating = this.$route.params.rating;
                console.log(this.ingredients);
                console.log(this.directions);
            },
            // mounted(){
            //     if (window.history && window.history.pushState) {
            //         history.pushState(null, null, document.URL);
            //         window.addEventListener('popstate', this.goBack, false);
            //     }
            // },
            // destroyed(){
            //     window.removeEventListener('popstate', this.goBack, false);
            // },

        }
    </script>

<style src="../assets/style-starter.css">
    
</style>
<style>
    #blur{
        height: 100%;
        background: rgba(251,235,235,.4); 
    }
    .el-carousel__container{
        height: 550px !important
    }
</style>
    



<template>
    <div id="blur">
    <section class="w3l-whyblock py-3">
        <el-container class="pb-lg-5 pb-md-4 pb-2">
            <el-header id="site-header" style="font-weight: bold;">
                    <nav class="navbar navbar-expand-lg navbar-light">
                        <a class="navbar-brand" style="color:grey; font-size: 25px;">
                            <i class="el-icon-back" @click="backhome()">Home </i>
                                <!-- <div class="headIcon" @click="backhome()">
                                </div> -->
                       </a>   
                    </nav>
               
            </el-header>
            <div class="row align-items-center m-0">
                <div class="col-lg-6 ps-0" style="margin-left:6%; margin-top:2%;">
                    <el-row>
                        <el-col :span=12>
                            <h4 class="title-style mb-4" style="float:center;font-weight:bold;color:darkred">No-Bake Nut Cookies</h4>
                            
                            <img src="../assets/images/ab.jpg" style="max-width: 60%;height: auto;"></el-col>
                        <el-col :span=12>
                            <h5 style="color:crimson; font-weight: bold;">Ingredients: </h5> <br/>
                            <li style="text-align: left;"> <i class="el-icon-star-off"></i>  1 c. firmly packed brown sugar</li>
                                <li style="text-align: left;"><i class="el-icon-star-off"></i>  1/2 c. evaporated milk</li>
                                
                                    <li style="text-align: left;"><i class="el-icon-star-off"></i> 1/2 tsp. vanilla</li> 
                                    <li style="text-align: left;"><i class="el-icon-star-off"></i>  1/2 c. broken nuts...</li>
                    
                        </el-col>
                       
                    </el-row> <el-divider></el-divider>
                    <div class="two-grids mt-3">
                        <h5 style="color:crimson">Descriptions</h5> <br/>
                        <div class="grids_info">
                            <i class="el-icon-star-off"></i>
                            <div class="detail">
                                
                                <p>Grease and flour 12-cup fluted tube pan or Bundt pan. In small bowl, mix walnuts, raisins, marshmallows and chocolate pieces.</p>
                            </div>
                        </div>
                        <div class="grids_info mt-xl-5 mt-lg-4 mt-5">
                            <i class="el-icon-star-off"></i>
                            <div class="detail">
                                <p>Grease and flour 12-cup fluted tube pan or Bundt pan. In small bowl, mix walnuts, raisins, marshmallows and chocolate pieces.</p>
                            </div>
                        </div>
                        <div class="grids_info mt-xl-5 mt-lg-4 mt-5">
                            <i class="el-icon-star-off"></i>
                            <div class="detail">
                         
                                <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                                    mollit.</p>
                            </div>
                        </div>
                        <div class="grids_info mt-xl-5 mt-lg-4 mt-5">
                            <i class="el-icon-star-off"></i>
                            <div class="detail">
                         
                                <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                                    mollit.</p>
                            </div>
                        </div>
                        <div class="grids_info mt-xl-5 mt-lg-4 mt-5">
                            <i class="el-icon-star-off"></i>
                            <div class="detail">
                         
                                <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                                    mollit.</p>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="col-lg-5 ps-0 ps-lg-4 mt-lg-0 mt-5">
                    <el-carousel indicator-position="outside">
                        <el-carousel-item v-for="item in 4" :key="item">
                            <img src="../assets/images/ab.jpg" alt="" style="height:100%; width:auto; border-radius: 10px;">
                        </el-carousel-item>
                    </el-carousel>
           </div>
        </div> 
        
    </el-container>
    </section>
    </div>
    </template>
    
    <script>
export default{
    name:'Test',
    data(){
        return{

        }
    },
    methods: {
        backhome(){
            this.$router.push({
                name: 'Homepage',  
            });
            window.location.reload();
        }
    },


  }
</script>

<style src="../assets/style-starter.css">
    
</style>
<style>
    .headIcon {
        width: 60px;
        height: 60px;
        background-image: url(../assets/images/cook_icon.png);
        background-size: cover;
    }
    #blur{
        height: 100%;
        background: rgba(251,235,235,.4); 
    }
    .el-form-item__content {
      display: flex;
      align-items: center;
    }
    .login_box{
        width: 75%;
        height: 100%;
        background-color: #ffffff;
        background: rgba(255, 255, 255, 0.6);
        z-index:1;
        opacity: 0.9;
        filter: alpha(opacity=90);
        border-radius: 20px;
        border:1px solid #ffffff;
        text-align: center;
        margin-left: 50%;
        margin-top:60%;
        padding-top: 5%;
        padding-bottom:5%;
        transform: translate(-50%,-50%);
        
    }
    .el-carousel__container{
        height: 550px !important
    }
</style>
    


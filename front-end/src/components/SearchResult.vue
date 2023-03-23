<template>
 <div id="blur">
    <el-container class="w3l-courses py-5" id="courses" style="padding-bottom:3%;">
        <el-header id="site-header" style="font-weight: bold;">
            <nav class="navbar navbar-expand-lg navbar-light">
                <a class="navbar-brand" style="color:grey; font-size: 25px; margin-left:5%;">
                    <i class="el-icon-back" @click="backhome()"> </i>
                    </a>   
                </nav>
            </el-header>
        <div class="container py-lg-0 py-md-0 py-0">
            <div class="row justify-content-center">
                <div v-for="(item,index) in showPage" :key="index" class="col-lg-4 col-md-6 item mt-5">
                    <el-card class="card">
                        <div class="card-header p-0 position-relative">
                            <a class="zoom d-block">
                                <!-- <img class="card-img-bottom d-block" src="../assets/images/rocky-road-cake.jpg" alt="Card image cap"> -->
                                <img :src="item.imagename" alt="Card image cap" class="card-img-bottom d-block" style="width: 332px; height:221px">
                            </a>
                        </div>
                        <div class="card-body course-details">
                            <a class="course-desc" @click="details(index)">{{ item.title }}
                            </a>
                        </div>
                        <div class="course-meta mt-4">
                                <div class="meta-item course-lesson">
                                    <p v-if="item.rating == null"> No rating yet </p>
                                    <el-rate
                                        v-else
                                        v-model="item.rating"
                                        disabled
                                        show-score
                                        text-color="#ff9900"
                                        score-template="{value} points"
                                        >
                                    </el-rate>
                                    
                                </div>
                        </div>
                    </el-card>
                </div>
            </div>
    </div>
            <div class="pagination-wrapper mt-5 pt-lg-3 text-center">
                <ul class="page-pagination">
                    <li><a class="next" @click="prev()">Previous</a></li>
                    <li v-for="(item,index) in getShowPage" :key="index" @click="page(item)">
                        <span v-if="item==currentPage" aria-current="page" class="page-numbers current">
                            {{ item }}
                        </span>
                        <a v-else class="page-numbers">{{ item }}</a>
                    </li>
                    <li><a v-if="totalPage!=getShowPage[getShowPage.length-1] " class="page-numbers">...</a></li>
                    <li><a class="next" @click="next()">Next</a></li>
                </ul>
                
            </div>
            <!-- //pagination -->
    </el-container>
    </div>
</template>

<script>// @ts-nocheck

const _ = require("lodash")
const frames = []
_.times(24, v => {
    frames.push(require(`../assets/images/cookimages/${v}.jpg`))
})
Array.prototype.contain = function(val)
{
     for (var i = 0; i < this.length; i++)
    {
       if (this[i] == val)
      {
       return true;
      }
    }
     return false;
};
export default{
    
    name:"SearchResult",
    data(){
        return{
            totalPage: '',
            currentPage: 1,
            pageSize: 6,
            showPage: [],
            result: [],   
        };
    },
    computed: {
        getShowPage:function(){ //计算指定显示页码数，这里以10页为例
          let arrList = []
          if(this.totalPage>10){
            for(let i=0; i<10; i++){
              arrList[i] = i+1;
            }
            return arrList
          }else{
            for(let i = 0; i<this.totalPage; i++){
              arrList[i] = i+1;
            }
            return arrList
          }
        }
    },
    methods: {
        randomlist(){
            var numbershow=Math.floor(Math.random()*frames.length);
            return numbershow;
        },
        backhome(){
            this.$router.push({
                name: 'Homepage',  
            });
            window.location.reload();
        },
        details(index){
            this.$router.push({
                name: 'Detail',  
                params:{
                    title: this.showPage[index].title,
                    ingredients: this.showPage[index].ingredients,
                    directions: this.showPage[index].directions,
                    rating: this.showPage[index].rating,
                }
            });
        },
        page(item){
            this.currentPage = item;
            if (this.currentPage == this.getShowPage[this.getShowPage.length - 1] && this.totalPage > this.currentPage) {
                for (let i = 0; i < this.getShowPage.length; i++) {
                    if (this.totalPage - this.getShowPage[this.getShowPage.length - 1] < 2) {
                        this.getShowPage[i] = this.getShowPage[i] + 1;
                    } else {
                        this.getShowPage[i] = this.getShowPage[i] + 2;
                    }
                }
            }
            if (this.currentPage == this.getShowPage[0] && this.currentPage > 1) {
                    for (let i = 0; i < this.getShowPage.length; i++) {
                    //这里是判断到头了
                        if (this.currentPage == 2) {
                            this.getShowPage[i] = this.getShowPage[i] - 1;
                        } else {
                            this.getShowPage[i] = this.getShowPage[i] - 2;
                        }
                    }
            }
            var list = (this.currentPage-1)*this.pageSize;  //每去一组数据的第一个索引
            
            this.showPage = this.result.slice(list,list+this.pageSize); //从总数据中取出每页的数据
        },
        prev(){
            if (this.currentPage!=1){
                this.currentPage --
                this.page(this.currentPage)
            }
        },
        next(){
            if (this.currentPage<this.totalPage){
                this.currentPage ++
                this.page(this.currentPage)
            }
        },

    },
    created(){
        this.result = this.$route.params.result;
        for(let i=0; i < this.result.length; i++){
            let index = this.randomlist();
            this.result[i].imagename = frames[index]
        }
        console.log(this.result[1].imagename)
        console.log(this.result[1].rating)
        this.totalPage = Math.ceil(this.result.length / this.pageSize);
        if (this.totalPage == 0){
            this.totalPage = 1
        }
        this.page(this.currentPage)
    }

}

</script>
<style src="../assets/style-starter.css">

</style>

<style>
 #blur{
        height: 100%;
        background: rgba(251,235,235,.4); 
    }
.el-form-item__content {
  display: flex;
  align-items: center;
}

</style>

<template>
    <div id="homepage">
        <div id="blur">
            <div class="demo-inner-content text-center">
                <el-row style="width: 100%;">
                    <div class="banner-info" style="float: center;">
                        <el-col :span=24>
                            <h5>Cooking is Easy</h5>
                            <h3>Passion For Cooking</h3> 
                        </el-col>  
                    </div>
                </el-row>
                <el-row style="margin-top:5%;">
                    <el-form :model="searchForm" :rules="searchrules" ref="searchForm">
                        <el-form-item prop="dish" style="display: inline-block;">
                            <el-input v-show="!suggest" type="input" v-model="searchForm.dish" prefix-icon="el-icon-knife-fork" 
                                    style="width: 300px; height: 40px; border-radius:30px 30px 30px 30px;" clearable 
                                    placeholder="Please input query"/>
                            <el-autocomplete 
                                v-show="suggest"
                                class="inline-input"
                                v-model="searchForm.dish"
                                :fetch-suggestions="focusInput"
                                placeholder="Please input query"
                                prefix-icon="el-icon-knife-fork"
                                style="width: 300px; height: 40px; border-radius:30px 30px 30px 30px;"
                                :trigger-on-focus="false"
                                @select="handleSelect"
                                clearable
                                required="true"
                            >
                            </el-autocomplete>
                        </el-form-item>
                        <el-form-item prop="include" style="display: inline-block;">
                            <el-input type="input" v-model="searchForm.include" prefix-icon="el-icon-question" style="width: 300px; height: 40px;" placeholder="Ingredients to include" />
                        </el-form-item>
                        <el-form-item prop="exclude" style="display: inline-block;">
                            <el-input type="input" v-model="searchForm.exclude" prefix-icon="el-icon-remove-outline" style="width: 300px; height: 40px;" placeholder="Ingredients to exclude" />
                        </el-form-item>
                        <br/>
                        <el-form-item style="display: inline-block;">
                            <el-switch
                            style="display: block"
                            v-model="value"
                            inactive-color="#808080"
                            active-color="#ff4949"
                            active-text="Search dish"
                            inactive-text="Search directions"
                            activate-value="dish"
                            inactivate-text="directions"
                            @change="changeStatus">
                            </el-switch>
                        </el-form-item>
                        <el-form-item style="display: inline-block;">
                            <el-button type="danger" size="large" style="width:200px;height: 40px;" @click="submitForm('searchForm')" round>Search</el-button>
                        </el-form-item>
                    </el-form>
        
                </el-row>
            </div>
        </div>
    </div>

</template>

<script>// @ts-nocheck
import axios from 'axios';
export default{
    name:"Homepage",
    data(){
        var vString=(rule, value, callback)=>{
            if (value == null || value == undefined || value == ""){
                callback()
            }
            else if (!(/\s*^[A-Za-z]/).test(value)){
                callback(new Error('Please enter string'))
            }
            else{
                callback()
            }
        }
        
        return{
            value: true,
            searchType: 'dish',
            suggestion: [],
            showSuggestion: false,
            listIndex: -1,
            suggest: true,
            result: [],
            searchForm: {
                    dish: '',
                    include: '',
                    exclude: ''
                },
            searchrules: {
                    dish: [
                        { validator: vString, trigger: 'blur',  message: 'Please enter query!'},],
                    include: [{ validator: vString, trigger: 'blur' },],
                    exclude: [{ validator: vString, trigger: 'blur' },],
                }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log(this.searchForm.dish)
                    if (this.searchType=='dish' && this.searchForm.dish == ''){
                        this.$message.error("Please enter the query field!") 
                    }
                    else if (this.searchForm.dish == '' && this.searchForm.include == '' && this.searchForm.exclude == ""){
                        this.$message.error("Please enter at least one field!") 
                    }
                    else{
                        const path = 'http://127.0.0.1:5000/index';
                        axios.post(path,{
                            dish: this.searchForm.dish,
                            include: this.searchForm.include,
                            exclude: this.searchForm.exclude,
                            searchType: this.searchType,
                        }).then((res)=>{
                            if (res.data.result.length==0){
                                this.$alert('No result found :( Please try another name', 'Error!', {
                                    confirmButtonText: 'Confirm',
                                });
                            }
                            else{
                                this.$router.push({
                                    name: 'SearchResult', 
                                    params: {
                                        result: res.data.result,
                                    }
                                }) 
                            }  
                            })
                        
                    }
                } 
                else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        changeStatus: function(callback){
            console.log(callback);
            if (callback==true){
                this.searchType = 'dish'
                this.suggest = true
            }
            else{
                this.searchType = 'directions'
                this.suggest = false
            }
            console.log(this.searchType);
        },
        focusInput(queryString, cb){
            if(this.searchType=='dish'){
                if (queryString && queryString.length>0){
                    const path = 'http://127.0.0.1:5000/suggestion';
                    axios.post(path,{
                        input: this.searchForm.dish
                    }).then((res)=>{
                        this.suggestion = res.data.suggestion

                        let result = this.suggestion.filter(dish => dish.indexOf(queryString) > -1)
                        console.log(result);
                        let suggestion = []
                        for (let i=0; i<result.length;i++){
                            console.log(result[i])
                             suggestion.push({
                                "value":result[i],
                                "address": ''});
                        }
                        console.log(result)
                        console.log(suggestion)
                        cb(suggestion);
                    })
                }
                else{
                    this.showSuggestion = false
                }
            }
        },
        handleSelect(item) {
            console.log(item);
        }
    },
}

</script>
<style src="../assets/style-starter.css">

</style>

<style>
.el-row {
    margin-bottom: 10px;
  }

#homepage{
    background:url("../assets/images/banner3.jpg");
    width:100%;
    height:100%;
    position:fixed;
    background-size:100% 100%;
}

#blur{
    height: 100%;
    background: rgba(0,0,0,.4); 
  /* can either be relative, absolute or fixed. If position is not set (i.e. static), it would be set to "relative" by script */
  /* to bound the empty top space created by inner element's top margin */
    width: 100%;
  /* background-color: #999; */
    display: grid;
    align-items: center;
}

.el-form-item__content {
  display: flex;
  align-items: center;
}

.el-form{
    width: 400px;
    height: auto;
    background: rgba(255,255,255,0.6);
    opacity: 0.9;
    filter: alpha(opacity=90);
    border-radius: 20px;
    text-align: center;
    justify-content: center;
    padding-top: 3%;
    text-justify: distribute-all-lines;
    display: inline-block;
    /* transform: translate(50%,-50%); */
}

/* .el-switch__label{
    color:crimson !important;
} */

.el-switch__label.el-switch__label--left.is-active{
    color:crimson !important;
}
.el-switch__label.el-switch__label--right.is-active{
    color:crimson !important;
}
</style>

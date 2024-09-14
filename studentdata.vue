<template>
  <div>
    <row>
      <Col span="16" offset="4">
        <row style="margin-top: 10px;">
          <Col span="4"><a href="javascript:void(0)" @click="this.$router.push('./teachers')">teacher data</a></Col>
          <Col span="20" style="text-align: right" ><a href="javascript:void(0)" @click="logout()">logout</a></Col>
        </row>
        <row style="text-align: center;display: inline"><h1> Student Grade List</h1></row>
        <row style="margin-top: 10px">
          <Col span="2" offset="8">
            <Button type="info" @click="get_students"> look up</Button>
          </Col>
          <Col span="2" offset="4">
            <Button type="success" @click="show_add">create</Button>
          </Col>
        </row>
        <row style="margin-top: 18px">
          <Col span="24">
            <Table :columns="columns" :data="data">
              <template #action="{row,index}">
                <Button type="primary" style="margin-right: 8px" size="small" @click="show_data(row)">edit</Button>
                <Button type="error" size="small" @click="delete_confirm(row)">Delete</Button>
              </template>
            </Table>
          </Col>
        </row>
      </Col>
    </row>
  </div>
  <div>
    <Modal
        v-model="add.modal"
        :loading="add.loading"
        title="Add a new student"
        @on-ok="add_confirm"
        @on-cancel="add_cancel">
        <p>
          <row>
            <Col span="4">Name:</Col>
            <Col span="20"><Input v-model="add.param.name" size="small" style="width: 80%"></Input></Col>
          </row>
        </p>
        <p>
          <row>
            <Col span="4" >Math:</Col>
            <Col span="20"><Input v-model="add.param.math" size="small" style="width: 80%"></Input></Col>
          </row>
        </p><p>
          <row>
            <Col span="4">English:</Col>
            <Col span="20"><Input v-model="add.param.english" size="small" style="width: 80%"></Input></Col>
          </row>
        </p><p>
          <row>
            <Col span="4">Physics:</Col>
            <Col span="20"><Input v-model="add.param.physics" size="small" style="width: 80%"></Input></Col>
          </row>
        </p>
        </Modal>
    <Modal
        v-model="edit.modal"
        :loading="edit.loading"
        title="edit a new student"
        @on-ok="edit_confirm"
        @on-cancel="edit_cancel">


      <p>
          <row>
            <Col span="4">Id:</Col>
            <Col span="20"><Input v-model="edit.param.id" disabled size="small" style="width: 80%"></Input></Col>
          </row>
        </p>
        <p>
          <row>
            <Col span="4">Name:</Col>
            <Col span="20"><Input v-model="edit.param.name" size="small" style="width: 80%"></Input></Col>
          </row>
        </p>
        <p>
          <row>
            <Col span="4" >Math:</Col>
            <Col span="20"><Input v-model="edit.param.math" size="small" style="width: 80%"></Input></Col>
          </row>
        </p><p>
          <row>
            <Col span="4">English:</Col>
            <Col span="20"><Input v-model="edit.param.english" size="small" style="width: 80%"></Input></Col>
          </row>
        </p><p>
          <row>
            <Col span="4">Physics:</Col>
            <Col span="20"><Input v-model="edit.param.physics" size="small" style="width: 80%"></Input></Col>
          </row>
        </p>
        </Modal>
  </div>
</template>
<script>
import {Button, Col, Input, Row} from "view-ui-plus";

export default {
  components: {Row, Input, Button, Col},
  data() {
    return{
    add:{
      loading:true,
      modal:false,
      param:{
        name:'',
        math:'',
        english:'',
        physics:'',
      },
    },
      edit:{
      loading:true,
      modal:false,
      param:{
        id:'',
        name:'',
        math:'',
        english:'',
        physics:'',
      },
    },
      columns:[{
        title:'student id',
        key:'id',
        align:'center'
      },{
        title:'Name',
        key:'name',
        align:'center'
      },{
        title:'Math',
        key:'math',
        align:'center'
      },{
        title:'English',
        key:'english',
        align:'center'
      },{
        title:'Physics',
        key:'physics',
        align:'center'
      },{
        title:'actions',
        slot:'action',
        minWidth:120
      },],
      data:[
      ]
    }

  },
  mounted() {
    this.get_students()
  },
  methods: {
    logout(){
      this.$axios({
        withCredentials: true,
        method: "POST",
        url: "http://localhost:9000/logout",
        data: JSON.stringify({}),
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((res) => {

        if (res.status !== 200) {
          this.$Message.error('API error+(' + res.status + ')');
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('/login')
          return
        }
        this.$Message.success(res.data.messages)
        this.$router.push('/login')
      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })
    },
    get_students()
    {
      this.data=[]
      console.log('get_students()')
      this.$axios({
        withCredentials: true,
        method: "GET",
        url: "http://localhost:9000/student_lists",
      }).then((res) => {
        console.log(res)
        if (res.status!==200){
          this.$Message.error('API error('+res.status+')')
          return
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('/login')
          return
        }
        if (res.data.code===0){
          this.data=res.data.data;

        }
        else{
          this.$Message.error('unable to access data('+res.data.message+')')

        }
      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })
    },
    show_add(){
      this.add.modal=true
    },
    add_confirm(){
    if (this.add.param.name==='') {
      this.$Message.error('Name cannot be empty')
      this.add.loading = false
      this.$nextTick(() => {
        this.add.loading = true
      })

    }
    let param={name:this.add.param.name}
    if(this.add.param.english!==''){
      param.english=this.add.param.english
    }if(this.add.param.math!==''){
      param.math=this.add.param.math
    }if(this.add.param.physics!==''){
      param.physics=this.add.param.physics
    }

    this.$axios({
        withCredentials: true,
        method: "POST",
        url: "http://localhost:9000/student_add",
        data: JSON.stringify(param),
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((res) => {
        console.log(res)
        if (res.status!==200) {
          this.$Message.error('API error+('+res.status+')')
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('/login')
          return
        }
        if (res.data.code!==0){
          this.$Message.error('error('+res.data.message+')')
          return;
        }
        this.add.modal=false
        this.add_reset();
        this.$Message.success(res.data.message)
        this.add.loading=false
        this.$nextTick(()=>{
          this.add.loading=true;
        })
        this.get_students();

      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })

    },
    add_reset(){
      this.add.param.physics=''
      this.add.param.name=''
      this.add.param.math=''
      this.add.param.english=''
      this.add.modal=false
    },
    add_cancel(){
      this.add_reset()

    },
    delete_confirm(row){
      const self=this
      this.$Modal.confirm({
        title:"confirm?",
        content:`Delete ${row.name}?`,
        onOk(){
          self.delete_submit(row.id)
        },
        onCancel(){
          return
        },
      })
    },
    delete_submit(id){
      const param={id:id}
      this.$axios({
        withCredentials: true,
        method: "POST",
        url: "http://localhost:9000/student_delete",
        data: JSON.stringify(param),
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((res) => {

        if (res.status !== 200) {

          this.$Message.error('API error+(' + res.status + ')');
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('/login')
          return
        }
        if (res.data.code!==0){
          this.$Message.error('error('+res.data.message+')')
          return;
        }
        this.$Message.success(res.data.message)
        this.get_students();

      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })
    },

    edit_reset(){
      this.edit.param.id='';
      this.edit.param.physics='';
      this.edit.param.name='';
      this.edit.param.math='';
      this.edit.param.english='';
    },
     show_data(row){
      this.edit_reset();
      this.edit.param.id=row.id;
      this.edit.param.physics=row.physics;
      this.edit.param.name=row.name;
      this.edit.param.math=row.math;
      this.edit.param.english=row.english;
      this.edit.modal=true;
    },
    edit_cancel(){
      this.edit_reset()
      this.edit.modal=false
    },
    edit_confirm()
    {
      this.edit.modal=true;
      if (this.edit.param.name==='') {
      this.$Message.error('Name cannot be empty')
      this.edit.loading = false
      this.$nextTick(() => {
        this.edit.loading = true
      })
      return
    }
    const param={
        id:this.edit.param.id,
        name:this.edit.param.name,
        math:this.edit.param.math,
        english:this.edit.param.english,
        physics:this.edit.param.physics,
    }

      this.$axios({
        withCredentials: true,
        method: "POST",
        url: "http://localhost:9000/student_edit",
        data: JSON.stringify(param),
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((res) => {

        if (res.status!==200) {
          this.$Message.error('API error+('+res.status+')')
          return;
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('/login')
          return
        }
        if (res.data.code!==0){
          this.$Message.error('error('+res.data.message+')')
          return;
        }
        this.edit.modal=false;
        this.edit_reset();
        this.$Message.success(res.data.message);
        this.edit.loading=false;
        this.$nextTick(()=>{
          this.edit.loading=true
        })
        this.get_students();

      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })
    },

  },
}
</script>
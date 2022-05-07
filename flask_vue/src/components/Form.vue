<template>
  <div class="form_box">
    <el-row :gutter="20" style="margin-top: 40px">
      <el-col :span="8" :offset="8">
        <el-form
          :model="ruleForm"
          :rules="rules"
          ref="ruleForm"
          label-width="100px"
          class="demo-ruleForm"
          status-icon
        >
          <el-form-item label="活动名称" prop="name">
            <el-input
              v-model="ruleForm.name"
              maxlength="10"
              show-word-limit
            ></el-input>
          </el-form-item>

          <el-form-item label="活动区域" prop="region">
            <el-select v-model="ruleForm.region" placeholder="请选择活动区域">
              <el-option label="北京" value="北京"></el-option>
              <el-option label="上海" value="上海"></el-option>
              <el-option label="广州" value="广州"></el-option>
              <el-option label="深圳" value="深圳"></el-option>
              <el-option label="厦门" value="厦门"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="活动时间" required>
            <el-col :span="11" class="colstyle">
              <el-form-item prop="date1">
                <el-date-picker
                  type="date"
                  placeholder="选择日期"
                  v-model="ruleForm.date1"
                  style="width: 100%"
                ></el-date-picker>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11" class="colstyle">
              <el-form-item prop="date2">
                <el-time-picker
                  placeholder="选择时间"
                  v-model="ruleForm.date2"
                  style="width: 100%"
                ></el-time-picker>
              </el-form-item>
            </el-col>
          </el-form-item>

          <el-form-item label="活动认证" prop="delivery">
            <el-switch v-model="ruleForm.delivery"></el-switch>
          </el-form-item>

          <el-form-item label="活动性质" prop="type">
            <el-checkbox-group v-model="ruleForm.type">
              <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
              <el-checkbox label="地推活动" name="type"></el-checkbox>
              <el-checkbox label="线下主题活动" name="type"></el-checkbox>
              <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item label="活动资源" prop="resource">
            <el-radio-group v-model="ruleForm.resource">
              <el-radio label="线上品牌商赞助"></el-radio>
              <el-radio label="线下场地免费"></el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="活动形式" prop="desc">
            <el-input
              type="textarea"
              :rows="6"
              v-model="ruleForm.desc"
              clearable
            ></el-input>
          </el-form-item>

          <el-form-item label="活动图片" prop="imageName">
            <!-- on-success:文件上传成功时的钩子，可用来赋值url
        before-upload: 上传文件之前的钩子，限制用户上传的图片格式和大小。
        on-preview：点击文件列表中已上传的文件时的钩子，可用来放大图片大小
        on-exceed：文件超出个数限制时的钩子，可配合limit限制个数。 -->
            <el-upload
              class="upload-demo"
              action="http://127.0.0.1:5000/User/SavePic"
              :on-success="handleAvatarSuccessPic"
              :before-upload="beforeAvatarUploadPic"
              :on-preview="handleCardPreviewPic"
              :on-exceed="handleExceedPic"
              accept=".jpg"
              :limit="1"
              list-type="picture"
            >
              <el-button size="small" type="primary">点击上传图片</el-button>
              <span style="margin-left: 20px" slot="tip" class="el-upload__tip"
                >只能上传jpg文件，且不超过2MB</span
              >
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
              <img width="100%" :src="dialogimageUrl" alt="" />
            </el-dialog>
          </el-form-item>

          <el-form-item label="活动文件" prop="fileName" class="form_file">
            <el-upload
              class="upload-demo"
              :on-success="handleAvatarSuccessFile"
              :before-upload="beforeAvatarUploadFile"
              :on-exceed="handleExceedFile"
              drag
              action="http://127.0.0.1:5000/User/SaveFile"
              multiple
              :limit="3"
              accept=".pdf, .doc, .docx, .rar, .zip, .exe, .pptx"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>，上传个数不超过3个
              </div>
            </el-upload>
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="ruleForm.email" clearable></el-input>
          </el-form-item>

          <el-form-item label="验证码" prop="captcha">
            <el-input v-model="ruleForm.captcha" clearable>
              <el-button
                slot="append"
                @click="sendMsg"
                type="info"
                :disabled="canClick"
                >{{ content }}</el-button
              >
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')"
              >立即创建</el-button
            >
            <el-button @click="resetForm('ruleForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Form",
  data() {
    return {
      ruleForm: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: "",
        imageName: [],
        fileName: [],
        email: "",
        captcha: "",
      },
      content: "发送验证码",
      totalTime: 10,
      canClick: false,
      dialogVisible: false,
      dialogimageUrl: "",
      rules: {
        name: [
          { required: true, message: "请输入活动名称", trigger: "blur" },
          {
            min: 3,
            max: 10,
            message: "长度在 3 到 10 个字符",
            trigger: "blur",
          },
        ],
        region: [
          { required: true, message: "请选择活动区域", trigger: "change" },
        ],
        date1: [
          {
            type: "date",
            required: true,
            message: "请选择日期",
            trigger: "change",
          },
        ],
        date2: [
          {
            type: "date",
            required: true,
            message: "请选择时间",
            trigger: "change",
          },
        ],
        type: [
          {
            type: "array",
            required: true,
            message: "请至少选择一个活动性质",
            trigger: "change",
          },
        ],
        resource: [
          { required: true, message: "请选择活动资源", trigger: "change" },
        ],
        desc: [{ required: true, message: "请填写活动形式", trigger: "blur" }],
        imageName: [
          { required: true, message: "请上传活动图片", trigger: "blur" },
        ],
        fileName: [
          { required: true, message: "请上传活动文件", trigger: "blur" },
        ],
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
        captcha: [{ required: true, message: "请输入验证码", trigger: "blur" }],
      },
    };
  },
  methods: {
    handleAvatarSuccessPic(res, file) {
      // this.uploadImgToBase64(file.raw).then((data) => {
      //     var imageobj = {};
      //     imageobj[file.name] = data.result;
      //     this.ruleForm.imageName.push(imageobj);
      //     console.log(this.ruleForm.imageName);
      // })
      this.ruleForm.imageName.push(file.name);
    },
    beforeAvatarUploadPic(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        this.$message({
          message: "上传的图片大小不能超过 2MB!",
          center: true,
          type: "error",
        });
      }
      return isLt2M;
    },
    handleExceedPic() {
      this.$message({
        message: "只能上传一张图片！",
        center: true,
        type: "error",
      });
    },
    handleCardPreviewPic(file) {
      this.dialogimage = file.url;
      this.dialogVisible = true;
    },
    handleAvatarSuccessFile(res, file) {
      // this.uploadImgToBase64(file.raw).then((data) => {
      //     var fileobj = {};
      //     fileobj[file.name] = data.result;
      //     this.ruleForm.fileName.push(fileobj);
      // })
      this.ruleForm.fileName.push(file.name);
    },
    beforeAvatarUploadFile(file) {
      const isLt2M = file.size / 1024 / 1024 < 20;
      if (!isLt2M) {
        this.$message({
          message: "上传的文件大小不能超过 20MB!",
          center: true,
          type: "error",
        });
      }
      return isLt2M;
    },
    handleExceedFile() {
      this.$message({
        message: "只能上传三个文件！",
        center: true,
        type: "error",
      });
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios
            .post("http://127.0.0.1:5000/User/FormSubmit", {
              ruleForm: this.ruleForm,
            })
            .then((response) => {
              if (response.data.code == 200) {
                this.$message({
                  message: "提交成功",
                  center: true,
                  type: "success",
                });
                this.timer = setInterval(() => {
                  this.$router.push({
                    name: "Home",
                  });
                }, 1000);
              } else if (response.data.code == 404) {
                this.$message({
                  message: "验证码输入错误，请重新尝试！",
                  center: true,
                  type: "error",
                });
              }
            });
        } else {
          this.$message({
            message: "存在字段未输入，请重新尝试！",
            center: true,
            type: "error",
          });
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    uploadImgToBase64(file) {
      // 核心方法，将图片转成base64字符串形式
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
          // 图片转base64完成后返回reader对象
          resolve(reader);
        };
        reader.onerror = reject;
      });
    },
    sendMsg() {
      if (this.ruleForm.email) {
        if (this.canClick) return;
        this.$message({
          message: "验证码发送成功！",
          center: true,
          type: "success",
        });
        this.$axios.post("http://127.0.0.1:5000/User/SendEmail", {
          email: this.ruleForm.email,
        });
        this.canClick = true;
        this.content = this.totalTime + "s后重新发送";
        let clock = window.setInterval(() => {
          this.totalTime--;
          this.content = this.totalTime + "s后重新发送";
          if (this.totalTime < 0) {
            window.clearInterval(clock);
            this.content = "重新发送验证码";
            this.totalTime = 10;
            this.canClick = false;
          }
        }, 1000);
      } else {
        this.$message({
          message: "邮箱未输入，请输入邮箱！",
          center: true,
          type: "error",
        });
      }
    },
  },
  beforeDestroy() {
    //清除定时器
    clearInterval(this.timer);
  },
  destroyed() {
    //清除定时器
    clearInterval(this.timer);
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
.form_box {
  width: 1500px;
  margin: 0 auto;
}
.colstyle {
  padding-left: 0px !important;
  padding-right: 0px !important;
}
.form_file .el-upload-dragger {
  width: 388px !important;
}
</style>

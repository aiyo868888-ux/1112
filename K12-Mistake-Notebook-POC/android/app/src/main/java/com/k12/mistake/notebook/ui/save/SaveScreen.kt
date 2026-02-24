package com.k12.mistake.notebook.ui.save

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SaveScreen(
    onSaveComplete: () -> Unit,
    onNavigateBack: () -> Unit
) {
    var questionText by remember { mutableStateOf("") }
    var wrongAnswer by remember { mutableStateOf("") }
    var correctAnswer by remember { mutableStateOf("") }
    var subject by remember { mutableStateOf("数学") }
    var isAnalyzing by remember { mutableStateOf(false) }
    var analysisResult by remember { mutableStateOf<String?>(null) }

    val subjects = listOf("数学", "物理", "化学", "英语", "语文", "生物", "历史", "地理")

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("保存错题") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, "返回")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 题目内容
            OutlinedTextField(
                value = questionText,
                onValueChange = { questionText = it },
                label = { Text("题目内容") },
                placeholder = { Text("OCR识别的题目内容...") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(150.dp),
                maxLines = 8
            )

            // 错误答案
            OutlinedTextField(
                value = wrongAnswer,
                onValueChange = { wrongAnswer = it },
                label = { Text("我的错误答案") },
                placeholder = { Text("填写你的错误答案...") },
                modifier = Modifier.fillMaxWidth(),
                maxLines = 3
            )

            // 正确答案
            OutlinedTextField(
                value = correctAnswer,
                onValueChange = { correctAnswer = it },
                label = { Text("正确答案（可选）") },
                placeholder = { Text("填写正确答案...") },
                modifier = Modifier.fillMaxWidth(),
                maxLines = 3
            )

            // 科目选择
            ExposedDropdownMenuBox(
                expanded = false,
                onExpandedChange = { }
            ) {
                OutlinedTextField(
                    value = subject,
                    onValueChange = { },
                    readOnly = true,
                    label = { Text("科目") },
                    trailingIcon = {
                        ExposedDropdownMenuDefaults.TrailingIcon(expanded = false)
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor()
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // AI分析按钮
            Button(
                onClick = {
                    isAnalyzing = true
                    // 模拟AI分析
                    kotlinx.coroutines.GlobalScope.launch {
                        kotlinx.coroutines.delay(2000)
                        analysisResult = """
                            错误类型：计算错误
                            知识点：一元二次方程
                            根本原因：学生对完全平方公式的特殊情况理解不够
                            改进建议：多做相关练习，加强基础概念的掌握
                        """.trimIndent()
                        isAnalyzing = false
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = questionText.isNotEmpty() && wrongAnswer.isNotEmpty() && !isAnalyzing
            ) {
                if (isAnalyzing) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("分析中...")
                } else {
                    Text("🧠 AI智能分析")
                }
            }

            // 分析结果
            if (analysisResult != null) {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.primaryContainer
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(
                            "AI分析结果",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                        )
                        Text(
                            analysisResult!!,
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            // 保存按钮
            Button(
                onClick = onSaveComplete,
                modifier = Modifier.fillMaxWidth(),
                enabled = questionText.isNotEmpty() && wrongAnswer.isNotEmpty()
            ) {
                Text("✓ 保存到错题本")
            }
        }
    }
}

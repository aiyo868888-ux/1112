package com.k12.mistake.notebook.ui.selection

import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import com.google.accompanist.permissions.ExperimentalPermissionsApi

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SelectionScreen(
    onSelectionComplete: () -> Unit,
    onNavigateBack: () -> Unit
) {
    var isDetecting by remember { mutableStateOf(true) }
    var questionRects by remember { mutableStateOf<List<QuestionRect>>(emptyList()) }
    var selectedRect by remember { mutableStateOf<QuestionRect?>(null) }

    // 模拟AI检测
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(1500)
        questionRects = listOf(
            QuestionRect(1, 100f, 150f, 300f, 200f),
            QuestionRect(2, 100f, 400f, 300f, 250f),
            QuestionRect(3, 100f, 700f, 300f, 200f)
        )
        isDetecting = false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("选择题目") },
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
        ) {
            // 检测状态提示
            if (isDetecting) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                        .background(
                            Color(0xFF2196F3),
                            RoundedCornerShape(8.dp)
                        )
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(24.dp),
                            color = Color.White
                        )
                        Text(
                            "AI正在检测题目区域...",
                            color = Color.White,
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            } else if (questionRects.isNotEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                        .background(
                            Color(0xFF4CAF50),
                            RoundedCornerShape(8.dp)
                        )
                        .padding(16.dp)
                ) {
                    Text(
                        "✓ 已检测到 ${questionRects.size} 个题目区域",
                        color = Color.White,
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
            }

            // 图片预览区域（带框选）
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .padding(16.dp)
                    .background(
                        Color.LightGray,
                        RoundedCornerShape(8.dp)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    "图片预览区域\n(显示拍摄的图片和框选)",
                    style = MaterialTheme.typography.bodyLarge,
                    color = Color.DarkGray
                )

                // 框选矩形（示例）
                questionRects.forEach { rect ->
                    val isSelected = selectedRect?.id == rect.id
                    Box(
                        modifier = Modifier
                            .offset(x = rect.x.dp, y = rect.y.dp)
                            .width(rect.width.dp)
                            .height(rect.height.dp)
                            .border(
                                3.dp,
                                if (isSelected) Color(0xFF10B981) else Color(0xFF4F46E5),
                                RoundedCornerShape(4.dp)
                            )
                            .background(
                                if (isSelected) Color(0xFF10B981).copy(alpha = 0.15f)
                                else Color(0xFF4F46E5).copy(alpha = 0.1f)
                            )
                            .clickable {
                                selectedRect = if (isSelected) null else rect
                            }
                            .zIndex(if (isSelected) 1f else 0f)
                    ) {
                        // 题号标签
                        Box(
                            modifier = Modifier
                                .offset(x = 0.dp, y = (-28).dp)
                                .background(
                                    if (isSelected) Color(0xFF10B981) else Color(0xFF4F46E5),
                                    RoundedCornerShape(4.dp)
                                )
                                .padding(horizontal = 12.dp, vertical = 4.dp)
                        ) {
                            Text(
                                "${rect.id}",
                                color = Color.White,
                                style = MaterialTheme.typography.titleSmall
                            )
                        }
                    }
                }
            }

            // 操作按钮
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                if (questionRects.isNotEmpty()) {
                    Text(
                        "已选择 ${questionRects.size} 个题目区域",
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedButton(
                        onClick = { /* 添加框选 */ },
                        modifier = Modifier.weight(1f)
                    ) {
                        Text("添加")
                    }

                    if (selectedRect != null) {
                        OutlinedButton(
                            onClick = {
                                selectedRect = null
                            },
                            modifier = Modifier.weight(1f),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = Color.Red
                            )
                        ) {
                            Text("删除选中")
                        }
                    }

                    Button(
                        onClick = onSelectionComplete,
                        modifier = Modifier.weight(1f),
                        enabled = questionRects.isNotEmpty()
                    ) {
                        Text("完成 (${questionRects.size})")
                    }
                }

                // 使用提示
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(12.dp)
                    ) {
                        Text(
                            "💡 操作提示",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            "• 系统已自动检测题目区域\n" +
                            "• 点击框选区域可以选中调整\n" +
                            "• 可以添加新的框选或删除不需要的\n" +
                            "• 调整完成后点击"完成"",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }
        }
    }
}

data class QuestionRect(
    val id: Int,
    val x: Float,
    val y: Float,
    val width: Float,
    val height: Float
)

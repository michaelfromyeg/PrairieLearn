const asyncHandler = require('express-async-handler');
const express = require('express');
const { pipeline } = require('node:stream/promises');
const { stringifyStream } = require('@prairielearn/csv');
const error = require('@prairielearn/error');
const sqldb = require('@prairielearn/postgres');

const sanitizeName = require('../../lib/sanitize-name');

const router = express.Router();
const sql = sqldb.loadSqlEquiv(__filename);

const setFilenames = function (locals) {
  const prefix = sanitizeName.questionFilenamePrefix(locals.question, locals.course);
  locals.questionStatsCsvFilename = prefix + 'stats.csv';
};

router.get(
  '/',
  asyncHandler(async (req, res) => {
    setFilenames(res.locals);
    const statsResult = await sqldb.queryAsync(sql.assessment_question_stats, {
      question_id: res.locals.question.id,
    });
    res.locals.assessment_stats = statsResult.rows;

    res.render(__filename.replace(/\.js$/, '.ejs'), res.locals);
  }),
);

router.get(
  '/:filename',
  asyncHandler(async (req, res) => {
    setFilenames(res.locals);

    if (req.params.filename === res.locals.questionStatsCsvFilename) {
      const cursor = await sqldb.queryCursor(sql.assessment_question_stats, {
        question_id: res.locals.question.id,
      });

      const stringifier = stringifyStream({
        header: true,
        columns: [
          'Course',
          'Instance',
          'Assessment',
          'Question number',
          'QID',
          'Question title',
          ...Object.values(res.locals.stat_descriptions).map((d) => d.non_html_title),
        ],
        transform(record) {
          return [
            record.course_short_name,
            record.course_instance_short_name,
            record.assessment_label,
            record.assessment_question_number,
            record.qid,
            record.question_title,
            record.mean_question_score,
            record.question_score_variance,
            record.discrimination,
            record.some_submission_perc,
            record.some_perfect_submission_perc,
            record.some_nonzero_submission_perc,
            record.average_first_submission_score,
            record.first_submission_score_variance,
            record.first_submission_score_hist,
            record.average_last_submission_score,
            record.last_submission_score_variance,
            record.last_submission_score_hist,
            record.average_max_submission_score,
            record.max_submission_score_variance,
            record.max_submission_score_hist,
            record.average_average_submission_score,
            record.average_submission_score_variance,
            record.average_submission_score_hist,
            record.submission_score_array_averages,
            record.incremental_submission_score_array_averages,
            record.incremental_submission_points_array_averages,
            record.average_number_submissions,
            record.number_submissions_variance,
            record.number_submissions_hist,
            record.quintile_question_scores,
          ];
        },
      });

      res.attachment(req.params.filename);
      await pipeline(cursor.stream(100), stringifier, res);
    } else {
      throw error.make(404, 'Unknown filename: ' + req.params.filename);
    }
  }),
);

module.exports = router;
